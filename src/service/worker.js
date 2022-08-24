import * as k from 'cdk8s';
import * as kplus from 'cdk8s-plus-22';
import createContainer from '../container.js';

/**
 * This function will create a worker manifest.
 * What this means is that this service should be used for applications that do not
 * need an ingress connected to them. I.e. a service that is only running standalone in the background.
 * One use case for this is i.e. you have a service that generate reports based on data it fetches from
 * a database, handles it, and publishes it somewhere.
 * TL;DR: This is not a service that needs access from the Internet. Such as an API.
 *
 * @param {object} app the app created by the main.js file
 * @param {object} inputs the inputs coming from the github action
 * @returns
 */
export default function createWorker(app, inputs) {
    const labels = {
        app: inputs.appName,
        'app.kubernetes.io/name': inputs.appName,
    };

    const chart = new k.Chart(app, inputs.appName + '-worker', {
        labels,
        namespace: inputs.namespace,
    });

    // Information https://kubernetes.io/docs/concepts/containers/
    const dockerContainer = createContainer(chart, inputs);

    // https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
    const deployment = new kplus.Deployment(chart, 'deployment', {
        select: false,
        containers: [dockerContainer],
        restartPolicy: kplus.RestartPolicy.ALWAYS,
        replicas: inputs.replicas,
        metadata: {
            name: inputs.appName,
            labels: labels,
            namespace: inputs.namespace,
        },
        podMetadata: {
            name: inputs.appName,
            labels: labels,
        },
    });

    if (inputs.nodegroup) {
        deployment.scheduling.attract(
            kplus.Node.labeled(
                kplus.NodeLabelQuery.is('instance', inputs.nodegroup || inputs.instance)
            )
        );
    }

    // This line will set the selector for the deployment to "app: <app_name>" to be static and not dynamic.
    // If it is dynamic, it will be a conflict with kubernetes immutability for deployments, and will block
    // the deployment from being deployed
    deployment.select(kplus.LabelSelector.of({ labels: { app: inputs.appName } }));

    // Return the manifest object
    return app;
}
