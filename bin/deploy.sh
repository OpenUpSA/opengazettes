#!/bin/bash
set -e

echo "Deploying to GitHub"

# add git auth
eval "$(ssh-agent -s)" #start the ssh agent
chmod 600 deploy_key # this key should have push access
ssh-add deploy_key

git config user.email "<webapps@code4sa.org>"
git config user.name "Open Gazettes (via TravisCI)"
git checkout ${TRAVIS_BRANCH}
git add _data _gazettes
git commit -m "Updated index via TravisCI [ci skip]"
git remote set-url origin git@github.com:code4sa/opengazettes.git
git push
