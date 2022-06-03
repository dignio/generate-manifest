import * as kplus from 'cdk8s-plus-22';
import * as secrets from '../imports/external-secrets.js';

/**
 * Create and populate the chart with the secrets location
 *
 * @param {object} chart the manifest chart
 * @param {object} inputs the github action inputs
 * @returns {object} The secret source for the docker container
 */
export default function createSecrets(chart, inputs) {
    if (!inputs.secretsmanager && !inputs.clusterName) {
        return {};
    }

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

    return { envFrom: [secretSource] };
}
