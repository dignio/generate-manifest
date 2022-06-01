import * as core from '@actions/core';
import createWebservice from './service/webservice.js';

const services = {
    webservice: createWebservice,
};

/**
 * This function selects the service based on what type
 * we are passing to the function.
 * This could be a generic webservice (currently just supporting this),
 * a cron job, some special service we have to create. Etc.
 *
 * @param {string} serviceType
 * @returns {function} The service chosen by the service type
 */
export default function GenerateManifest(serviceType) {
    const service = services[serviceType];

    if (service === undefined) {
        core.setFailed(` [!] No service type with name "${serviceType}" found!`);

        // Return a noop function
        return () => {};
    }

    // Return the service
    return service;
}
