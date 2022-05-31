/**
 * Get the pod resources based on a size string to simplify this for the end user.
 * i.e. container_size: "medium"
 *
 * @param {string} size the size of the instance
 * @returns
 */
export default function getResources(size) {
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
        // 0.5GB / 0.25vCPU, which is the default instance
        return [0.5, 250];
    }

    return resources[size];
}
