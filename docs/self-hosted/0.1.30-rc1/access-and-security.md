# Access, HTTPS, and MFA

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Use a secure first connection

The application should remain bound to `127.0.0.1:8080`. Before public DNS and
HTTPS are ready, use an administrator-controlled SSH tunnel:

```shell
ssh -L 8080:127.0.0.1:8080 admin@server.example.com
```

Then open `http://127.0.0.1:8080/login` on the administrator workstation. Do not
use browser login over public plain HTTP.

## Configure a panel hostname and HTTPS

Create a customer-controlled DNS record for the panel hostname pointing to the
server. Review the package's Nginx proxy and replace `server_name _` with that
exact hostname.

On a fresh Ubuntu host, the stock Nginx site and the Snotic proxy both declare a
default server. Remove the stock enabled-site link only when its target and file
checksum still match the unmodified `nginx-common` package conffile:

!!! danger
    Removing an enabled Nginx site changes request routing. Stop if the checksum
    comparison fails, the link points elsewhere, or this is not the fresh host
    accepted by the preflight. Review the existing web-server configuration
    instead of deleting it.

```shell
set -eu
default_conf=/etc/nginx/sites-available/default
if test -L /etc/nginx/sites-enabled/default; then
  expected_md5="$(dpkg-query -W -f='${Conffiles}\n' nginx-common | awk '$1 == "/etc/nginx/sites-available/default" {print $2}')"
  test -n "$expected_md5"
  test "$(readlink -f /etc/nginx/sites-enabled/default)" = "$default_conf"
  test "$(md5sum "$default_conf" | awk '{print $1}')" = "$expected_md5"
  sudo rm -- /etc/nginx/sites-enabled/default
fi
```

Then enable the reviewed Snotic proxy:

```shell
sudoedit /etc/nginx/sites-available/hipanel.conf
sudo ln -s /etc/nginx/sites-available/hipanel.conf /etc/nginx/sites-enabled/hipanel.conf
sudo nginx -t
sudo systemctl reload nginx
```

If the Snotic symlink already exists and points to the reviewed file, do not
create a second one. The package does not change firewall or DNS policy.

After DNS resolves correctly and ports 80 and 443 are authorized:

```shell
sudo certbot --nginx --redirect -d panel.example.com -m admin@example.com --agree-tos --non-interactive
sudo certbot renew --dry-run
sudo systemctl status certbot.timer
```

Replace the synthetic hostname and email. Sign in at
`https://panel.example.com/login`.

## Browser sessions

- Sign in with the local Snotic administrator username and password.
- Use **Sign out** when finished.
- Sessions expire after 12 hours.
- Resetting the account password from the server invalidates existing browser
  sessions.
- Never place an API key or legacy token in the panel URL.

## Enable MFA

MFA is optional and disabled by default.

1. Open **Security** and select **Enable MFA**.
2. Enter the shared current-password field.
3. Select **Show QR Code**.
4. Scan the code in a TOTP authenticator, or enter the manual key.
5. Enter the current authenticator code and select **Enable MFA**.
6. Store the recovery codes shown once in an approved password manager.

MFA is not active until the authenticator code is confirmed. Once enabled, the
login flow asks for an authenticator or unused recovery code. When MFA is off,
that field is not shown.

Use **Regenerate Recovery Codes** to replace all existing recovery codes. Use
**Disable MFA** with the current password and an authenticator or recovery code
to return to password-only login.

## Change or recover the password

Use **Security > Change Password** when the current password is known. Other
sessions are invalidated; the current session remains active.

For a lost password, create another protected temporary file through authorized
SSH access and run the root-only reset command:

```shell
sudo install -m 0600 -o root -g root /dev/null /root/snotic-admin-password-reset
sudo sh -c 'umask 077; python3 -c "import secrets; print(secrets.token_urlsafe(32))" > /root/snotic-admin-password-reset'
sudo /opt/hipanel/bin/hipanel auth reset-password -config /etc/hipanel/config.json -username admin -password-file /root/snotic-admin-password-reset
sudo cat /root/snotic-admin-password-reset
sudo rm -f /root/snotic-admin-password-reset
```

The reset preserves the account's MFA setting and invalidates its existing
sessions.
