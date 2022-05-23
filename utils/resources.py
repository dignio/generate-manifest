def get_resources(size="") -> tuple[str, str]:
    """This function will return a tuple with the resources we should
    allocate the docker container

    Example from the manifest:
    resources:
        requests:
          memory: "1.5Gi"
          cpu: "1000m"
        limits:
          memory: "1.5Gi"
          cpu: "1000m"

    This will be CapacityProvisioned=1vCPU 2GB for the Fargate instance.

    Note: Fargate always add 0.5Gi of memory by default, so 1.5Gi would equal 2Gi
    TODO: Review these instances and adjust accordingly
    """

    # (memory in Gi, CPU in millis)
    if size == "small":
        return (0.5, 500)
    elif size == "medium":
        return (1.5, 1000)
    elif size == "large":
        return (2.5, 1000)
    elif size == "xlarge":
        return (3.5, 2000)
    else:
        return (0.001, 250)  # 0.5GB / 0.25vCPU, which is the default instance
