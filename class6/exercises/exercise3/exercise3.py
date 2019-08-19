import logging
from getpass import getpass
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking


PASSWORD = getpass()
LOGGER = logging.getLogger("nornir")


def main():
    LOGGER.info("Script initalizing...")
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    for host, data in nr.inventory.hosts.items():
        data.password = PASSWORD
    LOGGER.critical("Passwords set, commence automation!")
    nr.run(
        task=networking.netmiko_send_command, command_string="show mac address-table"
    )
    LOGGER.error("Oh no! We're all out of automation tasks :(")
    LOGGER.debug("Hey, what are you still doing here?")


if __name__ == "__main__":
    main()
