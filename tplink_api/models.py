from dataclasses import dataclass


# @dataclass
# class Request:
#     url: str
#     headers: dict = None
#     data: dict = None


@dataclass
class Device:
    name: str
    ip_addr: str
    mac_addr: str


@dataclass
class DisplayStatus:
    internet_conn_status: int
    wireless_clients_count: int
    wire_clients_count: int
    operation_mode: int
    working_mode: int


@dataclass
class InternetInfo:
    wan_conn_type: str
    wan_mac: str
    wan_ip: str
    wan_gateway: str
