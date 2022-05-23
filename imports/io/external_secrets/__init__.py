import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdk8s
import constructs


class ExternalSecret(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="iokubernetes-client.ExternalSecret",
):
    '''
    :schema: ExternalSecret
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        spec: "ExternalSecretSpec",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''Defines a "ExternalSecret" API object.

        :param scope: the scope in which to define this object.
        :param id: a scope-local name for the object.
        :param spec: 
        :param metadata: 
        '''
        props = ExternalSecretProps(spec=spec, metadata=metadata)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        spec: "ExternalSecretSpec",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> typing.Any:
        '''Renders a Kubernetes manifest for "ExternalSecret".

        This can be used to inline resource manifests inside other objects (e.g. as templates).

        :param spec: 
        :param metadata: 
        '''
        props = ExternalSecretProps(spec=spec, metadata=metadata)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        '''Renders the object to Kubernetes JSON.'''
        return typing.cast(typing.Any, jsii.invoke(self, "toJson", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        '''Returns the apiVersion and kind for "ExternalSecret".'''
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


@jsii.data_type(
    jsii_type="iokubernetes-client.ExternalSecretProps",
    jsii_struct_bases=[],
    name_mapping={"spec": "spec", "metadata": "metadata"},
)
class ExternalSecretProps:
    def __init__(
        self,
        *,
        spec: "ExternalSecretSpec",
        metadata: typing.Optional[cdk8s.ApiObjectMetadata] = None,
    ) -> None:
        '''
        :param spec: 
        :param metadata: 

        :schema: ExternalSecret
        '''
        if isinstance(spec, dict):
            spec = ExternalSecretSpec(**spec)
        if isinstance(metadata, dict):
            metadata = cdk8s.ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "spec": spec,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def spec(self) -> "ExternalSecretSpec":
        '''
        :schema: ExternalSecret#spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("ExternalSecretSpec", result)

    @builtins.property
    def metadata(self) -> typing.Optional[cdk8s.ApiObjectMetadata]:
        '''
        :schema: ExternalSecret#metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[cdk8s.ApiObjectMetadata], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="iokubernetes-client.ExternalSecretSpec",
    jsii_struct_bases=[],
    name_mapping={
        "backend_type": "backendType",
        "controller_id": "controllerId",
        "data": "data",
        "data_from": "dataFrom",
        "key_vault_name": "keyVaultName",
        "kv_version": "kvVersion",
        "project_id": "projectId",
        "region": "region",
        "role_arn": "roleArn",
        "template": "template",
        "type": "type",
        "vault_mount_point": "vaultMountPoint",
        "vault_role": "vaultRole",
    },
)
class ExternalSecretSpec:
    def __init__(
        self,
        *,
        backend_type: typing.Optional["ExternalSecretSpecBackendType"] = None,
        controller_id: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Sequence["ExternalSecretSpecData"]] = None,
        data_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_vault_name: typing.Optional[builtins.str] = None,
        kv_version: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        template: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
        vault_mount_point: typing.Optional[builtins.str] = None,
        vault_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_type: Determines which backend to use for fetching secrets.
        :param controller_id: The ID of controller instance that manages this ExternalSecret. This is needed in case there is more than a KES controller instances within the cluster.
        :param data: 
        :param data_from: 
        :param key_vault_name: Used by: azureKeyVault.
        :param kv_version: Vault K/V version either 1 or 2, default = 2.
        :param project_id: Used by: gcpSecretsManager.
        :param region: Used by: secretsManager, systemManager.
        :param role_arn: Used by: alicloudSecretsManager, secretsManager, systemManager.
        :param template: Template which will be deep merged without mutating any existing fields. into generated secret, can be used to set for example annotations or type on the generated secret
        :param type: DEPRECATED: Use spec.template.type.
        :param vault_mount_point: Used by: vault.
        :param vault_role: Used by: vault.

        :schema: ExternalSecretSpec
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backend_type is not None:
            self._values["backend_type"] = backend_type
        if controller_id is not None:
            self._values["controller_id"] = controller_id
        if data is not None:
            self._values["data"] = data
        if data_from is not None:
            self._values["data_from"] = data_from
        if key_vault_name is not None:
            self._values["key_vault_name"] = key_vault_name
        if kv_version is not None:
            self._values["kv_version"] = kv_version
        if project_id is not None:
            self._values["project_id"] = project_id
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if template is not None:
            self._values["template"] = template
        if type is not None:
            self._values["type"] = type
        if vault_mount_point is not None:
            self._values["vault_mount_point"] = vault_mount_point
        if vault_role is not None:
            self._values["vault_role"] = vault_role

    @builtins.property
    def backend_type(self) -> typing.Optional["ExternalSecretSpecBackendType"]:
        '''Determines which backend to use for fetching secrets.

        :schema: ExternalSecretSpec#backendType
        '''
        result = self._values.get("backend_type")
        return typing.cast(typing.Optional["ExternalSecretSpecBackendType"], result)

    @builtins.property
    def controller_id(self) -> typing.Optional[builtins.str]:
        '''The ID of controller instance that manages this ExternalSecret.

        This is needed in case there is more than a KES controller instances within the cluster.

        :schema: ExternalSecretSpec#controllerId
        '''
        result = self._values.get("controller_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.List["ExternalSecretSpecData"]]:
        '''
        :schema: ExternalSecretSpec#data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.List["ExternalSecretSpecData"]], result)

    @builtins.property
    def data_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: ExternalSecretSpec#dataFrom
        '''
        result = self._values.get("data_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key_vault_name(self) -> typing.Optional[builtins.str]:
        '''Used by: azureKeyVault.

        :schema: ExternalSecretSpec#keyVaultName
        '''
        result = self._values.get("key_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kv_version(self) -> typing.Optional[jsii.Number]:
        '''Vault K/V version either 1 or 2, default = 2.

        :schema: ExternalSecretSpec#kvVersion
        '''
        result = self._values.get("kv_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Used by: gcpSecretsManager.

        :schema: ExternalSecretSpec#projectId
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Used by: secretsManager, systemManager.

        :schema: ExternalSecretSpec#region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Used by: alicloudSecretsManager, secretsManager, systemManager.

        :schema: ExternalSecretSpec#roleArn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Any:
        '''Template which will be deep merged without mutating any existing fields.

        into generated secret, can be used to set for example annotations or type on the generated secret

        :schema: ExternalSecretSpec#template
        '''
        result = self._values.get("template")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''DEPRECATED: Use spec.template.type.

        :schema: ExternalSecretSpec#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_mount_point(self) -> typing.Optional[builtins.str]:
        '''Used by: vault.

        :schema: ExternalSecretSpec#vaultMountPoint
        '''
        result = self._values.get("vault_mount_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_role(self) -> typing.Optional[builtins.str]:
        '''Used by: vault.

        :schema: ExternalSecretSpec#vaultRole
        '''
        result = self._values.get("vault_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="iokubernetes-client.ExternalSecretSpecBackendType")
class ExternalSecretSpecBackendType(enum.Enum):
    '''Determines which backend to use for fetching secrets.

    :schema: ExternalSecretSpecBackendType
    '''

    SECRETS_MANAGER = "SECRETS_MANAGER"
    '''secretsManager.'''
    SYSTEM_MANAGER = "SYSTEM_MANAGER"
    '''systemManager.'''
    VAULT = "VAULT"
    '''vault.'''
    AZURE_KEY_VAULT = "AZURE_KEY_VAULT"
    '''azureKeyVault.'''
    GCP_SECRETS_MANAGER = "GCP_SECRETS_MANAGER"
    '''gcpSecretsManager.'''
    ALICLOUD_SECRETS_MANAGER = "ALICLOUD_SECRETS_MANAGER"
    '''alicloudSecretsManager.'''
    IBMCLOUD_SECRETS_MANAGER = "IBMCLOUD_SECRETS_MANAGER"
    '''ibmcloudSecretsManager.'''


@jsii.data_type(
    jsii_type="iokubernetes-client.ExternalSecretSpecData",
    jsii_struct_bases=[],
    name_mapping={
        "is_binary": "isBinary",
        "key": "key",
        "name": "name",
        "path": "path",
        "property": "property",
        "recursive": "recursive",
        "secret_type": "secretType",
        "version": "version",
        "version_id": "versionId",
        "version_stage": "versionStage",
    },
)
class ExternalSecretSpecData:
    def __init__(
        self,
        *,
        is_binary: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        property: typing.Optional[builtins.str] = None,
        recursive: typing.Optional[builtins.bool] = None,
        secret_type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
        version_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_binary: Whether the backend secret shall be treated as binary data represented by a base64-encoded string. You must set this to true for any base64-encoded binary data in the backend - to ensure it is not encoded in base64 again. Default is false. Default: false.
        :param key: Secret key in backend.
        :param name: Name set for this key in the generated secret.
        :param path: Path from SSM to scrape secrets This will fetch all secrets and use the key from the secret as variable name.
        :param property: Property to extract if secret in backend is a JSON object.
        :param recursive: Allow to recurse thru all child keys on a given path, default false.
        :param secret_type: Used by: ibmcloudSecretsManager Type of secret - one of username_password, iam_credentials or arbitrary.
        :param version: Used by: gcpSecretsManager.
        :param version_id: Used by: secretsManager.
        :param version_stage: Used by: alicloudSecretsManager, secretsManager.

        :schema: ExternalSecretSpecData
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if is_binary is not None:
            self._values["is_binary"] = is_binary
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path
        if property is not None:
            self._values["property"] = property
        if recursive is not None:
            self._values["recursive"] = recursive
        if secret_type is not None:
            self._values["secret_type"] = secret_type
        if version is not None:
            self._values["version"] = version
        if version_id is not None:
            self._values["version_id"] = version_id
        if version_stage is not None:
            self._values["version_stage"] = version_stage

    @builtins.property
    def is_binary(self) -> typing.Optional[builtins.bool]:
        '''Whether the backend secret shall be treated as binary data represented by a base64-encoded string.

        You must set this to true for any base64-encoded binary data in the backend - to ensure it is not encoded in base64 again. Default is false.

        :default: false.

        :schema: ExternalSecretSpecData#isBinary
        '''
        result = self._values.get("is_binary")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Secret key in backend.

        :schema: ExternalSecretSpecData#key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name set for this key in the generated secret.

        :schema: ExternalSecretSpecData#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path from SSM to scrape secrets This will fetch all secrets and use the key from the secret as variable name.

        :schema: ExternalSecretSpecData#path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def property(self) -> typing.Optional[builtins.str]:
        '''Property to extract if secret in backend is a JSON object.

        :schema: ExternalSecretSpecData#property
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recursive(self) -> typing.Optional[builtins.bool]:
        '''Allow to recurse thru all child keys on a given path, default false.

        :schema: ExternalSecretSpecData#recursive
        '''
        result = self._values.get("recursive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Used by: ibmcloudSecretsManager Type of secret - one of username_password, iam_credentials or arbitrary.

        :schema: ExternalSecretSpecData#secretType
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Used by: gcpSecretsManager.

        :schema: ExternalSecretSpecData#version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Used by: secretsManager.

        :schema: ExternalSecretSpecData#versionId
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_stage(self) -> typing.Optional[builtins.str]:
        '''Used by: alicloudSecretsManager, secretsManager.

        :schema: ExternalSecretSpecData#versionStage
        '''
        result = self._values.get("version_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalSecretSpecData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ExternalSecret",
    "ExternalSecretProps",
    "ExternalSecretSpec",
    "ExternalSecretSpecBackendType",
    "ExternalSecretSpecData",
]

publication.publish()
