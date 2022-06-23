import * as k from 'cdk8s';
import CronJob from '../../imports/cronjob.js';
import createContainer from '../container.js';
import createSecrets from '../secrets.js';

/**
 * This function will create the node group selection
 *
 * @param {object} inputs the inputs coming from the github action
 * @returns {object} the node group selection object
 */
function assignToNodeGroup(inputs) {
    if (inputs.fargate) {
        return {};
    }

    // If we are not running on fargate, select the AWS EKS Node Group
    return {
        affinity: {
            nodeAffinity: {
                requiredDuringSchedulingIgnoredDuringExecution: {
                    nodeSelectorTerms: [
                        {
                            matchExpressions: [
                                { key: 'instance', operator: 'In', values: [inputs.instance] },
                            ],
                        },
                    ],
                },
            },
        },
    };
}

/**
 * This function will create a cronjob manifest.
 *
 * @param {object} app the app created by the main.js file
 * @param {object} inputs the inputs coming from the github action
 * @returns {object} app
 */
export default function createCronJob(app, inputs) {
    const labels = {
        app: inputs.appName,
        'app.kubernetes.io/name': inputs.appName,
    };

    const chart = new k.Chart(app, inputs.appName + '-cronjob', {
        labels,
        namespace: inputs.namespace,
    });

    // The docker container configuration
    // Information https://kubernetes.io/docs/concepts/containers/
    const dockerContainer = createContainer(chart, inputs);

    // This is the main object for our cronjob manifest. Also known as a workload resource.
    // https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
    const cronJobProperties = {
        metadata: {
            name: inputs.appName,
            labels: labels,
            namespace: inputs.namespace,
        },
        spec: {
            schedule: inputs.schedule,
            jobTemplate: {
                spec: {
                    template: {
                        spec: {
                            ...assignToNodeGroup(inputs),
                            // Never restart the cronjob if it fails,
                            // wait until the next run.
                            restartPolicy: 'Never',
                            containers: [dockerContainer],
                        },
                    },
                },
            },
        },
    };

    new CronJob(chart, 'cronjob', cronJobProperties);

    // create the secret manifest files
    createSecrets(chart, inputs);

    // Return the manifest object
    return app;
}
