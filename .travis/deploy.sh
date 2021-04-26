#!/bin/bash

# scripts/deploy.sh
# Deploy code from travis

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
# chmod 600 .travis/id_rsa # Allow read access to the private key
# ssh-add .travis/id_rsa # Add the private key to SSH

git config --global push.default matching
git remote add deploy ssh://travis@$IP:$PORT$DEPLOY_DIR
git push deploy master

# Skip this command if you don't need to execute any additional commands after deploying.
ssh travis@$IP -p $PORT <<EOF
    cd $DEPLOY_DIR
    crystal build --release --no-debug index.cr # Change to whatever commands you need!
EOF
  exit
else
  # do nothing
  exit
fi
