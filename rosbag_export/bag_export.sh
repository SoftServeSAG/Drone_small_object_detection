#!/bin/bash


helpFunction()
{
   echo ""
   echo "Usage: $0 -rosbag parameterA -topic parameterB -out parameterC"
   echo -e "\t-r [r]osbag file"
   echo -e "\t-t [t]opic of image"
   echo -e "\t-o [o]utput folder"
   exit 1 # Exit script after printing help
}



while getopts "r:t:o:" opt
do
   case "$opt" in
      r ) rosbag_file="$OPTARG" ;;
      t ) rostopic_image="$OPTARG" ;;
      o ) output_folder="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$rosbag_file" ] || [ -z "$rostopic_image" ] || [ -z "$output_folder" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

if_is_link=`readlink $0`
command_name=$0
if [[ if_is_link ]]; then
  command_name=$if_is_link
fi

MY_PATH=`dirname "$if_is_link"`
MY_PATH=`( cd "$MY_PATH" && pwd )`
cd $MY_PATH

# remove the old link
rm .tmuxinator.yml

# link the session file to .tmuxinator.yml
ln session.yml .tmuxinator.yml

# start tmuxinator
tmuxinator start session rosbag_file="$rosbag_file" rostopic_image="$rostopic_image" output_folder="$output_folder"
