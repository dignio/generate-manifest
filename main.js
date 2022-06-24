import * as k from 'cdk8s';
import * as core from '@actions/core';

import generateManifest from './src/strategy.js';

const DEVELOPMENT = process.env.DEVELOPMENT === 'true';

// All inputs coming from the action
// Integers and booleans are transformed from strings to int/bool using JSON.parse
const inputs = {
    // Required
    appName: core.getInput('app_name', { required: true }),
    namespace: core.getInput('namespace', { required: true }),
    serviceType: core.getInput('service_type', { required: true }),
    dockerImage: core.getInput('docker_image', { required: true }),
    instance: core.getInput('instance', { required: true }),

    // Optional
    nodegroup: core.getInput('nodegroup', { required: false }),
    containerPort: JSON.parse(core.getInput('container_port') || null),
    port: JSON.parse(core.getInput('port') || null),
    replicas: JSON.parse(core.getInput('replicas') || '1'),
    clusterName: core.getInput('cluster_name') || null,
    containerSize: core.getInput('container_size') || null,
    containerCommand: JSON.parse(core.getInput('container_command') || null),
    containerArgs: JSON.parse(core.getInput('container_args') || null),
    secretsmanager: JSON.parse(core.getInput('secretsmanager') || 'false'),
    fargate: JSON.parse(core.getInput('fargate') || 'true'),
    // The cronjob schedule
    // https://crontab.guru/
    schedule: core.getInput('schedule') || null,
};

const app = new k.App();

core.info(` [*] Creating manifest files for ${inputs.appName}`);

try {
    // This will populate the app object
    generateManifest(inputs.serviceType)(app, inputs);

    // Base64 encode the yaml
    const buff = new Buffer.from(app.synthYaml());
    const base64data = buff.toString('base64');

    // Create the output manifest yaml
    core.setOutput('manifest', base64data);

    if (DEVELOPMENT) {
        console.log(app.synthYaml());
    }
} catch (error) {
    console.error(error);

    core.setFailed(error.message);
}
