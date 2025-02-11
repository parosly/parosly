from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.configs import _globals, relabel
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
    kuma,
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
)
from src.models.prometheus.misc import auth, tls


class ScrapeConfig(BaseModel):
    job_name: str = Field(..., description="The job name assigned to scraped metrics by default.")
    scrape_interval: str | None = Field(
        _globals.GlobalConfig.__getattribute__(_globals.GlobalConfig(), "scrape_interval"),
        description="How frequently to scrape targets from this job.",
    )
    scrape_timeout: str | None = Field(
        _globals.GlobalConfig.__getattribute__(_globals.GlobalConfig(), "scrape_timeout"),
        description="Per-scrape timeout when scraping this job.",
    )
    scrape_protocols: list[str] | None = Field(
        _globals.GlobalConfig.__getattribute__(_globals.GlobalConfig(), "scrape_protocols"),
        description="The protocols to negotiate during a scrape with the client.",
    )
    scrape_classic_histograms: bool | None = Field(
        False,
        description="Whether to scrape a classic histogram that is also exposed as a native histogram. "
        "(has no effect without --enable-feature=native-histograms)",
    )
    metrics_path: str | None = Field(
        "/metrics", description="The HTTP resource path on which to fetch metrics from targets."
    )
    honor_labels: bool | None = Field(
        False,
        description="Controls how Prometheus handles conflicts between labels that are already present in "
        "scraped data and labels that Prometheus would attach server-side.",
    )
    honor_timestamps: bool | None = Field(
        True, description="Controls whether Prometheus respects the timestamps present in scraped data."
    )
    track_timestamps_staleness: bool | None = Field(
        False,
        description="Controls whether Prometheus tracks staleness of the metrics that have explicit timestamps "
        "present in scraped data.",
    )
    scheme: str | None = Field("http", description="Configures the protocol scheme used for requests.")
    params: dict[str, list[str]] | None = Field(None, description="Optional HTTP URL parameters.")
    enable_compression: bool | None = Field(
        True, description="If set to false, Prometheus will request uncompressed response from the scraped target."
    )
    basic_auth: auth.BasicAuthConfig | None = Field(
        None,
        description="Sets the `Authorization` header on every scrape request with the "
        "configured username and password.",
    )
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Sets the `Authorization` header on every scrape request with the configured credentials."
    )
    oauth2: auth.OAuth2Config | None = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.",
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether scrape requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")
    tls_config: tls.TLSConfig | None = Field(None, description="Configures the scrape request's TLS settings.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded "
        "from proxying. IP and domain names can contain port numbers.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    azure_sd_configs: list[azure.AzureSDConfig] | None = Field(
        None, description="List of Azure service discovery configurations."
    )
    consul_sd_configs: list[consul.ConsulSDConfig] | None = Field(
        None, description="List of Consul service discovery configurations."
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
    kuma_sd_configs: list[kuma.KumaControlPlaneConfig] | None = Field(
        None, description="List of Kuma service discovery configurations."
    )
    lightsail_sd_configs: list[lightsail.LightsailAPIConfig] | None = Field(
        None, description="List of Lightsail service discovery configurations."
    )
    linode_sd_configs: list[linode.LinodeAPIConfig] | None = Field(
        None, description="List of Linode service discovery configurations."
    )
    marathon_sd_configs: list[marathon.MarathonConfig] | None = Field(
        None, description="List of Marathon service discovery configurations."
    )
    nerve_sd_configs: list[nerve.NerveSDConfig] | None = Field(
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
    static_configs: list[static.StaticConfig] | None = Field(
        None, description="List of labeled statically configured targets for this job."
    )
    relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None, description="List of target relabel configurations."
    )
    metric_relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None, description="List of metric relabel configurations."
    )
    body_size_limit: str | None = Field(
        "0", description="An uncompressed response body larger than this many bytes will cause the scrape to fail."
    )
    sample_limit: int | None = Field(
        0, description="Per-scrape limit on number of scraped samples that will be accepted."
    )
    label_limit: int | None = Field(
        0, description="Per-scrape limit on number of labels that will be accepted for a sample."
    )
    label_name_length_limit: int | None = Field(
        0, description="Per-scrape limit on length of labels name that will be accepted for a sample."
    )
    label_value_length_limit: int | None = Field(
        0, description="Per-scrape limit on length of labels value that will be accepted for a sample."
    )
    target_limit: int | None = Field(
        0, description="Per-scrape config limit on number of unique targets that will be accepted."
    )
    keep_dropped_targets: int | None = Field(
        0, description="Per-job limit on the number of targets dropped by relabeling that will be kept in memory."
    )
    native_histogram_bucket_limit: int | None = Field(
        0, description="Limit on total number of positive and negative buckets allowed in a single native histogram."
    )
    native_histogram_min_bucket_factor: float | None = Field(
        0, description="Lower limit for the growth factor of one bucket to the next in each native histogram."
    )
