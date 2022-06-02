import * as k from 'cdk8s';
import * as kplus from 'cdk8s-plus-22';
import * as secrets from '../../imports/external-secrets.js';
import getResources from '../resources.js';

/**
 * This function will create a webservice manifest.
 *
 * @param {object} app the app created by the main.js file
 * @param {*} inputs the inputs coming from the github action
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

    const [memory, cpu] = getResources(inputs.containerSize);

    // The docker container configuration
    // Information https://kubernetes.io/docs/concepts/containers/
    const dockerContainer = {
        name: inputs.appName,
        image: inputs.dockerImage,
        port: inputs.containerPort,
        command: JSON.parse(inputs.containerCommand),
        args: JSON.parse(inputs.containerArgs),

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

        // Information regarding resources
        // https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        resources: {
            cpu: {
                limit: kplus.Cpu.millis(cpu),
                request: kplus.Cpu.millis(cpu),
            },
            memory: {
                limit: k.Size.gibibytes(memory),
                request: k.Size.gibibytes(memory),
            },
        },

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

    if (inputs.secretsmanager && inputs.clusterName) {
        // We are using this service to handle the external secrets coming from
        // AWS Secrets Manager: https://github.com/external-secrets/external-secrets
        // it will fetch data from `cluster/cluster_name/app_name`.
        // This will transform all key values to env vars for the deployment
        new secrets.ExternalSecret(chart, 'external-secret', {
            metadata: {
                name: inputs.appName,
                namespace: inputs.namespace,
            },
            spec: {
                backendType: secrets.ExternalSecretSpecBackendType.SECRETS_MANAGER,
                dataFrom: [`cluster/${inputs.clusterName}/${inputs.appName}`],
            },
        });

        // Information regarding secrets
        // https://kubernetes.io/docs/concepts/configuration/secret/
        const secret = new kplus.Secret(chart, 'secret', {
            metadata: {
                name: inputs.appName,
            },
        });

        const secretSource = kplus.Env.fromSecret(secret);

        // assign the secrets created in kubernetes by external secret to the container
        Object.assign(dockerContainer, { envFrom: [secretSource] });
    }

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

    deployment.select(kplus.LabelSelector.of({ labels: { app: inputs.appName } }));

    // The service to expose our pod/application to the Internet
    // https://kubernetes.io/docs/concepts/services-networking/service/
    const service = new kplus.Service(chart, 'service', {
        ports: [{ port: 5000, targetPort: 5000 }],
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
