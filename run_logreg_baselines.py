import os

if int(os.getenv('USE_AGG', 0)) == 1:
    import matplotlib
    matplotlib.use('Agg')

import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score

from oaprogression.training import baselines
from oaprogression.evaluation import stats

if __name__ == "__main__":
    args = baselines.init_args()
    train_folds, metadata_test, seed = baselines.init_metadata(args)
    os.makedirs(args.save_dir, exist_ok=True)

    results = {}
    for feature_set in [['AGE', 'SEX', 'BMI'],
                        ['KL', ],
                        ['AGE', 'SEX', 'BMI', 'KL'],
                        ['AGE', 'SEX', 'BMI', 'KL', 'SURG', 'INJ', 'WOMAC']]:

        models_best, mean_std_best, cv_scores = baselines.build_logreg_model(train_folds, feature_set, seed,
                                                                             args.n_vals_c, average_precision_score)
        print('CV score:', feature_set, cv_scores)
        test_res = baselines.eval_logreg(metadata_test, feature_set, models_best, mean_std_best)
        features_suffix = '_'.join(feature_set)
        plt.rcParams.update({'font.size': 16})

        y_test = metadata_test.Progressor.values.copy() > 0
        ids = metadata_test.ID.values
        sides = metadata_test.Side.values
        stats.roc_curve_bootstrap(y_test,
                                  test_res,
                                  n_bootstrap=args.n_bootstrap,
                                  savepath=os.path.join(args.save_dir,
                                                        f'ROC_MOST_BL_all_{features_suffix}.pdf'))

        results[f'preds_MOST_BL_all_{features_suffix}'] = (ids, sides, y_test, test_res)

    with open(os.path.join(args.save_dir, 'results_baselines.pkl'), 'wb') as f:
        pickle.dump(results, f)



