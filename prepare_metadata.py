import argparse
import os
from oaprogression.metadata import oai
from oaprogression.metadata import most

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--oai_meta', default='')
    parser.add_argument('--most_meta', default='')
    args = parser.parse_args()

    os.makedirs('Metadata', exist_ok=True)
    if not os.path.isfile(os.path.join('Metadata', 'OAI_progression.csv')):
        oai_meta = oai.build_img_progression_meta(args.oai_meta)
        oai_meta.to_csv(os.path.join('Metadata', 'OAI_progression.csv'), index=None)
    else:
        print('OAI progression metadata exists!')

    if not os.path.isfile(os.path.join('Metadata', 'OAI_participants.csv')):
        oai_participants = oai.build_clinical(args.oai_meta)
        oai_participants.to_csv(os.path.join('Metadata', 'OAI_participants.csv'), index=None)
    else:
        print('OAI participants metadata exists!')

    if not os.path.isfile(os.path.join('Metadata', 'MOST_progression.csv')):
        most_meta = most.build_img_progression_meta(args.most_meta)
        #most_meta.to_csv(os.path.join('Metadata', 'MOST_progression.csv'), index=None)