from middlewared.alert.base import Alert, AlertLevel, AlertSource


class HTTPDBindAddressAlertSource(AlertSource):
    level = AlertLevel.WARNING
    title = "The Web UI Could Not Bind to Specified Address"

    async def check(self):
        settings = await self.middleware.call("datastore.query", "system.settings", None, {"get": True})
        address = settings["stg_guiaddress"]
        with open("/usr/local/etc/nginx/nginx.conf") as f:
            # XXX: this is parse the file instead of slurping in the contents
            # (or in reality, just be moved somewhere else).
            if (f.read().find("0.0.0.0") != -1 and
                    address not in ("0.0.0.0", "")):
                # XXX: IPv6
                return Alert(
                    "The web UI could bot bind to %s; using wildcard",
                    address,
                )
