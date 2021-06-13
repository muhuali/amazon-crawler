#!/bin/bash -x
#

echo y | gcloud compute instances create chrome-remote-desktop  --metadata-from-file startup-script=./chrome_desktop/instance_startup.sh --zone us-west1-a --machine-type=e2-small
