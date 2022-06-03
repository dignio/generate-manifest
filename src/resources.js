import * as k from 'cdk8s';
import * as kplus from 'cdk8s-plus-22';

/**
 * Get the pod resources based on a size string to simplify this for the end user.
 * i.e. container_size: "medium"
 *
 * @param {string} size the size of the instance
 * @returns {array} The resources array
 */
function getResources(size) {
    /**
     * This function will return a tuple with the resources we should
     * allocate the docker container
     *
     * Example from the manifest:
     * resources:
     *      requests:
     *      memory: "1.5Gi"
     *      cpu: "1000m"
     *      limits:
     *      memory: "1.5Gi"
     *      cpu: "1000m"
     *
     * This will be CapacityProvisioned=1vCPU 2GB for the Fargate instance.
     *
     * Note: Fargate always add 0.5Gi of memory by default, so 1.5Gi would equal 2Gi
     * TODO: Review these instances and adjust accordingly
     *
     */

    // [memory in Gi, CPU in millis]
    const resources = {
        small: [0.5, 500],
        medium: [1.5, 1000],
        large: [2.5, 1000],
        xlarge: [3.5, 2000],
    };

    if (resources[size] === undefined) {
        // This will fallback to 0.5GB / 0.25vCPU, which is the default fargate instance
        return [0, 0];
    }

    return resources[size];
}

/**
 * Create the resource object for the docker container
 *
 * @param {string} size the size of the instance
 * @returns {object} The resources for the container
 */
export default function createResources(containerSize) {
    const [memory, cpu] = getResources(containerSize);

    // if these are not set to 0 (aka false)
    if (cpu && memory) {
        // Information regarding resources
        // https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        return {
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
        };
    }

    // Return an empty object. This will not add the resources to the container object,
    // which means it is using the default set
    return {};
}
