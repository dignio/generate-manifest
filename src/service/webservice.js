import * as k from 'cdk8s';
import * as kplus from 'cdk8s-plus-22';
import createResources from '../resources.js';
import createSecrets from '../secrets.js';

/**
 * This function will create a webservice manifest.
 *
 * @param {object} app the app created by the main.js file
 * @param {object} inputs the inputs coming from the github action
 * @returns
 */
export default function createWebservice(app, inputs) {
    const labels = {
        app: inputs.appName,
        'app.kubernetes.io/name': inputs.appName,
    };

    const chart = new k.Chart(app, inputs.appName + '-webservice', {
        labels,
        namespace: inputs.namespace,
    });

    // The docker container configuration
    // Information https://kubernetes.io/docs/concepts/containers/
    const dockerContainer = {
        name: inputs.appName,
        image: inputs.dockerImage,
        port: inputs.containerPort,
        command: inputs.containerCommand,
        args: inputs.containerArgs,

        // Information regarding liveness and readiness
        // https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
        liveness: kplus.Probe.fromTcpSocket({
            failureThreshold: 3,
            periodSeconds: k.Duration.seconds(15),
            timeoutSeconds: k.Duration.seconds(60),
            port: inputs.containerPort,
        }),
        readiness: kplus.Probe.fromTcpSocket({
            failureThreshold: 3,
            periodSeconds: k.Duration.seconds(15),
            timeoutSeconds: k.Duration.seconds(60),
            port: inputs.containerPort,
        }),

        // Information regarding security context
        // https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
        securityContext: {
            ensureNonRoot: true,
            // https://hub.armo.cloud/docs/c-0017
            // if we set this to true, it is not possible to write to /tmp
            readOnlyRootFilesystem: false,
            privileged: false,
            user: 1000,
            group: 3000,
            // https://hub.armo.cloud/docs/c-0016
            allowPrivilegeEscalation: false,
        },
    };

    // assign it to the container object
    Object.assign(dockerContainer, createResources(inputs.containerSize));

    // assign the secrets created in kubernetes by external secret to the container
    Object.assign(dockerContainer, createSecrets(chart, inputs));

    // This is the main object for our deployment manifest. Also
    // known as a workload resource.
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
        securityContext: {
            ensureNonRoot: true,
            // https://hub.armo.cloud/docs/c-0013
            runAsUser: 1000,
            runAsGroup: 3000,
            fsGroup: 2000,
        },
    });

    // This line will set the selector for the deployment to "app: <app_name>" to be static and not dynamic.
    // If it is dynamic, it will be a conflict with kubernetes immutability for deployments, and will block
    // the deployment from being deployed
    deployment.select(kplus.LabelSelector.of({ labels: { app: inputs.appName } }));

    // The service to expose our pod/application to the Internet
    // https://kubernetes.io/docs/concepts/services-networking/service/
    const service = new kplus.Service(chart, 'service', {
        ports: [{ port: inputs.port, targetPort: inputs.containerPort }],
        metadata: {
            name: inputs.appName,
            labels: labels,
            namespace: inputs.namespace,
            // The alb ingress target type is set to IP so the ALB can create
            // a target group with the service IP to allow traffic to the pod
            annotations: { 'alb.ingress.kubernetes.io/target-type': 'ip' },
        },
        type: kplus.ServiceType.NODE_PORT,
    });

    service.selectLabel('app', inputs.appName);

    // Return the manifest object
    return app;
}
