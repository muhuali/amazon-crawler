# /bin/bash


for i in {1..20}
do
    echo "Start deleting instances"
    echo Y | gcloud compute instances delete my-app-instance my-app-instance-2 my-app-instance-3 my-app-instance-4 my-app-instance-5 --zone=us-west1-a
    echo "Deletion Completed"
    sleep 20
    echo y | gcloud compute instances create my-app-instance my-app-instance-2 my-app-instance-3 my-app-instance-4 my-app-instance-5 --metadata-from-file startup-script=startup.sh --zone us-west1-a
    echo "Creation Completed!"
    sleep 450
done