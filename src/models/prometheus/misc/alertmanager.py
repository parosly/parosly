from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.configs import relabel
from src.models.prometheus.discovery import (
    aws,
    azure,
    consul,
    digitalocean,
    dns,
    docker,
    eureka,
    file_sd,
    gce,
    hetzner,
    http,
    ionos,
    kubernetes,
    lightsail,
    linode,
    marathon,
    nerve,
    nomad,
    openstack,
    ovhcloud,
    puppetdb,
    scaleway,
    serverset,
    static,
    triton,
    uyuni,
    vultr,
)
from src.models.prometheus.misc import auth, tls


class AlertmanagerConfig(BaseModel):
    timeout: str | None = Field("10s", description="Per-target Alertmanager timeout when pushing alerts.")
    api_version: str | None = Field("v2", description="The API version of Alertmanager.")
    path_prefix: str | None = Field("/", description="Prefix for the HTTP path alerts are pushed to.")
    scheme: str | None = Field("http", description="Configures the protocol scheme used for requests.")
    basic_auth: auth.BasicAuthConfig | None = Field(
        None, description="Sets the `Authorization` header on every request with the configured username and password."
    )
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Optional `Authorization` header configuration."
    )
    sigv4: auth.Sigv4Config | None = Field(
        None, description="Optionally configures AWS's Signature Verification 4 signing process to sign requests."
    )
    oauth2: auth.OAuth2Config | None = Field(None, description="Optional OAuth 2.0 configuration.")
    tls_config: tls.TLSConfig | None = Field(None, description="Configures the scrape request's TLS settings.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded "
        "from proxying.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")
    azure_sd_configs: list[azure.AzureSDConfig] | None = Field(
        None, description="List of Azure service discovery configurations."
    )
    consul_sd_configs: list[consul.ConsulSDConfig] | None = Field(
        None, description="List of Consul service discovery configurations."
    )
    dns_sd_configs: list[dns.DNSSDConfig] | None = Field(
        None, description="List of DNS service discovery configurations."
    )
    ec2_sd_configs: list[aws.EC2SDConfig] | None = Field(
        None, description="List of EC2 service discovery configurations."
    )
    eureka_sd_configs: list[eureka.EurekaSDConfig] | None = Field(
        None, description="List of Eureka service discovery configurations."
    )
    file_sd_configs: list[file_sd.FileSDConfig] | None = Field(
        None, description="List of file service discovery configurations."
    )
    digitalocean_sd_configs: list[digitalocean.DigitalOceanSDConfig] | None = Field(
        None, description="List of DigitalOcean service discovery configurations."
    )
    docker_sd_configs: list[docker.DockerSDConfig] | None = Field(
        None, description="List of Docker service discovery configurations."
    )
    dockerswarm_sd_configs: list[docker.DockerSwarmSDConfig] | None = Field(
        None, description="List of Docker Swarm service discovery configurations."
    )
    gce_sd_configs: list[gce.GCESDConfig] | None = Field(
        None, description="List of GCE service discovery configurations."
    )
    hetzner_sd_configs: list[hetzner.HetznerSDConfig] | None = Field(
        None, description="List of Hetzner service discovery configurations."
    )
    http_sd_configs: list[http.HttpSDConfig] | None = Field(
        None, description="List of HTTP service discovery configurations."
    )
    ionos_sd_configs: list[ionos.IONOSCloudConfig] | None = Field(
        None, description="List of IONOS service discovery configurations."
    )
    kubernetes_sd_configs: list[kubernetes.KubernetesSDConfig] | None = Field(
        None, description="List of Kubernetes service discovery configurations."
    )
    lightsail_sd_configs: list[lightsail.LightsailAPIConfig] | None = Field(
        None, description="List of Lightsail service discovery configurations."
    )
    linode_sd_configs: list[list[linode.LinodeAPIConfig]] | None = Field(
        None, description="List of Linode service discovery configurations."
    )
    marathon_sd_configs: list[list[marathon.MarathonConfig]] | None = Field(
        None, description="List of Marathon service discovery configurations."
    )
    nerve_sd_configs: list[list[nerve.NerveSDConfig]] | None = Field(
        None, description="List of AirBnB's Nerve service discovery configurations."
    )
    nomad_sd_configs: list[nomad.NomadSDConfig] | None = Field(
        None, description="List of Nomad service discovery configurations."
    )
    openstack_sd_configs: list[openstack.OpenStackSDConfig] | None = Field(
        None, description="List of OpenStack service discovery configurations."
    )
    ovhcloud_sd_configs: list[ovhcloud.OVHcloudSDConfig] | None = Field(
        None, description="List of OVHcloud service discovery configurations."
    )
    puppetdb_sd_configs: list[puppetdb.PuppetDBSDConfig] | None = Field(
        None, description="List of PuppetDB service discovery configurations."
    )
    scaleway_sd_configs: list[scaleway.ScalewaySDConfig] | None = Field(
        None, description="List of Scaleway service discovery configurations."
    )
    serverset_sd_configs: list[serverset.ServersetSDConfig] | None = Field(
        None, description="List of Zookeeper Serverset service discovery configurations."
    )
    triton_sd_configs: list[triton.TritonSDConfig] | None = Field(
        None, description="List of Triton service discovery configurations."
    )
    uyuni_sd_configs: list[uyuni.UyuniSDConfig] | None = Field(
        None, description="List of Uyuni service discovery configurations."
    )
    vultr_sd_configs: list[vultr.VultrSDConfig] | None = Field(
        None, description="List of Vultr service discovery configurations."
    )
    static_configs: list[static.StaticConfig] | None = Field(
        None, description="List of labeled statically configured Alertmanagers."
    )
    relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None, description="List of Alertmanager relabel configurations."
    )
    alert_relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None, description="List of alert relabel configurations."
    )
