import * as k from 'cdk8s';
import * as kplus from 'cdk8s-plus-22';
import createResources from './resources.js';
import createSecrets from './secrets.js';

/**
 * This function will create the docker container object.
 *
 * @param {object} chart the chart
 * @param {object} inputs the inputs coming from the github action
 * @returns {object} the docker container object
 */
export default function createContainer(chart, inputs) {
    const dockerContainer = {
        name: inputs.appName,
        image: inputs.dockerImage,
        command: inputs.containerCommand,
        args: inputs.containerArgs,
    };

    // The following is not available for the cronjob and worker docker container
    if (['cronjob', 'worker'].indexOf(inputs.serviceType) === -1) {
        Object.assign(dockerContainer, {
            port: inputs.containerPort,
        });

        // Information regarding liveness and readiness
        // https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
        Object.assign(dockerContainer, {
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
        });

        // Information regarding security context
        // https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
        Object.assign(dockerContainer, {
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
        });
    }

    if (inputs.serviceType !== 'cronjob') {
        // assign it to the container object
        Object.assign(dockerContainer, createResources(inputs.containerSize));

        // create the secret manifest files
        Object.assign(dockerContainer, createSecrets(chart, inputs));
    }

    // For the special handling of cronjobs
    if (inputs.serviceType === 'cronjob') {
        // assign the secrets if activated
        if (inputs.secretsmanager && inputs.clusterName) {
            Object.assign(dockerContainer, {
                envFrom: [{ secretRef: { name: inputs.appName } }],
            });
        }
    }

    return dockerContainer;
}
