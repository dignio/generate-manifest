// generated by cdk8s
import { ApiObject } from 'cdk8s';
/**
 *
 *
 * @schema ExternalSecret
 */
export class ExternalSecret extends ApiObject {
    /**
     * Returns the apiVersion and kind for "ExternalSecret"
     */
    static GVK = {
        apiVersion: 'kubernetes-client.io/v1',
        kind: 'ExternalSecret',
    };
    /**
     * Renders a Kubernetes manifest for "ExternalSecret".
     *
     * This can be used to inline resource manifests inside other objects (e.g. as templates).
     *
     * @param props initialization props
     */
    static manifest(props) {
        return {
            ...ExternalSecret.GVK,
            ...toJson_ExternalSecretProps(props),
        };
    }
    /**
     * Defines a "ExternalSecret" API object
     * @param scope the scope in which to define this object
     * @param id a scope-local name for the object
     * @param props initialization props
     */
    constructor(scope, id, props) {
        super(scope, id, {
            ...ExternalSecret.GVK,
            ...props,
        });
    }
    /**
     * Renders the object to Kubernetes JSON.
     */
    toJson() {
        const resolved = super.toJson();
        return {
            ...ExternalSecret.GVK,
            ...toJson_ExternalSecretProps(resolved),
        };
    }
}
/**
 * Converts an object of type 'ExternalSecretProps' to JSON representation.
 */
/* eslint-disable max-len, quote-props */
export function toJson_ExternalSecretProps(obj) {
    if (obj === undefined) {
        return undefined;
    }
    const result = {
        spec: toJson_ExternalSecretSpec(obj.spec),
        metadata: obj.metadata,
    };
    // filter undefined values
    return Object.entries(result).reduce(
        (r, i) => (i[1] === undefined ? r : { ...r, [i[0]]: i[1] }),
        {}
    );
}
/**
 * Converts an object of type 'ExternalSecretSpec' to JSON representation.
 */
/* eslint-disable max-len, quote-props */
export function toJson_ExternalSecretSpec(obj) {
    if (obj === undefined) {
        return undefined;
    }
    const result = {
        controllerId: obj.controllerId,
        type: obj.type,
        template: obj.template,
        backendType: obj.backendType,
        vaultRole: obj.vaultRole,
        vaultMountPoint: obj.vaultMountPoint,
        kvVersion: obj.kvVersion,
        keyVaultName: obj.keyVaultName,
        dataFrom: obj.dataFrom?.map((y) => y),
        data: obj.data?.map((y) => toJson_ExternalSecretSpecData(y)),
        roleArn: obj.roleArn,
        region: obj.region,
        projectId: obj.projectId,
    };
    // filter undefined values
    return Object.entries(result).reduce(
        (r, i) => (i[1] === undefined ? r : { ...r, [i[0]]: i[1] }),
        {}
    );
}
/* eslint-enable max-len, quote-props */
/**
 * Determines which backend to use for fetching secrets
 *
 * @schema ExternalSecretSpecBackendType
 */
export var ExternalSecretSpecBackendType;
(function (ExternalSecretSpecBackendType) {
    /** secretsManager */
    ExternalSecretSpecBackendType['SECRETS_MANAGER'] = 'secretsManager';
    /** systemManager */
    ExternalSecretSpecBackendType['SYSTEM_MANAGER'] = 'systemManager';
    /** vault */
    ExternalSecretSpecBackendType['VAULT'] = 'vault';
    /** azureKeyVault */
    ExternalSecretSpecBackendType['AZURE_KEY_VAULT'] = 'azureKeyVault';
    /** gcpSecretsManager */
    ExternalSecretSpecBackendType['GCP_SECRETS_MANAGER'] = 'gcpSecretsManager';
    /** alicloudSecretsManager */
    ExternalSecretSpecBackendType['ALICLOUD_SECRETS_MANAGER'] = 'alicloudSecretsManager';
    /** ibmcloudSecretsManager */
    ExternalSecretSpecBackendType['IBMCLOUD_SECRETS_MANAGER'] = 'ibmcloudSecretsManager';
})(ExternalSecretSpecBackendType || (ExternalSecretSpecBackendType = {}));
/**
 * Converts an object of type 'ExternalSecretSpecData' to JSON representation.
 */
/* eslint-disable max-len, quote-props */
export function toJson_ExternalSecretSpecData(obj) {
    if (obj === undefined) {
        return undefined;
    }
    const result = {
        key: obj.key,
        name: obj.name,
        property: obj.property,
        isBinary: obj.isBinary,
        path: obj.path,
        recursive: obj.recursive,
        secretType: obj.secretType,
        version: obj.version,
        versionStage: obj.versionStage,
        versionId: obj.versionId,
    };
    // filter undefined values
    return Object.entries(result).reduce(
        (r, i) => (i[1] === undefined ? r : { ...r, [i[0]]: i[1] }),
        {}
    );
}
/* eslint-enable max-len, quote-props */