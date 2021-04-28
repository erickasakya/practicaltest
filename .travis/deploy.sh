#!/bin/bash

APP="$0"
BRANCH="$1"

if [ "$1" = "" ]; then
  echo "To deploy, you must specify the branch
  ./deploy.sh [staging|production]"
  exit
elif [ "$1" = "staging" ] ; then
  # deploy to staging
  exit
elif [ "$BRANCH" = "production" ]; then
  # deploy to production
eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/trtravis_key # Allow read access to the private key
ssh-add .travis/trtravis_key # Add the private key to SSH
ssh -i .travis/trtravis_key travis@$IP pwd

git config --global push.default matching
git remote add deploy ssh://travis@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh travis@$IP -p $PORT <<EOF
    cd $DEPLOY_DIR
    source /home/travis/virtualenv/practicaltestenv/bin/activate
    pip install -r requirements.txt
     
EOF
  exit
else
  # do nothing
  exit
fi
