# Big Give notifier

Sends slack updates about how the Big Give is going.

## Setup

1. You’ll need to set up a slack workflow that runs on webhook trigger, and sends a message containing the data it receives
2. You’ll need to add the trigger URL as a repo secret called `SLACK_TRIGGER_URL`
3. Uncomment the schedule stuff in the GitHub workflow
