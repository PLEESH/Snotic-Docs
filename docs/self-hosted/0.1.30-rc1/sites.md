# Manage WordPress Sites

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Follow operation progress

Long actions show progress beside the control that started them. While an
operation is active, its button and conflicting controls are disabled. Keep the
operation ID and inspect **Ops** before retrying a request that appears stuck.

## Create a site in the browser

1. Open **Create Site**.
2. Enter the domain without a URL scheme or path.
3. Leave **Root path** empty for `/var/www/<domain>`, or enter the intended
   managed path.
4. Enter the WordPress title, administrator username, email, and password.
5. Keep **Install WordPress** selected for an ordinary WordPress site.
6. Select **Issue Let's Encrypt cert** only after DNS points to this server.
7. Select **Create Site** once and follow the inline operation progress.

**Metadata only** registers a site without provisioning its operating-system,
web, database, or WordPress resources. Use it only for an intentional advanced
workflow.

## Create a site with the CLI

Keep the WordPress password out of shell history and process arguments:

```shell
sudo install -m 0600 -o root -g root /dev/null /root/wordpress-admin-password
sudo sh -c 'umask 077; python3 -c "import secrets; print(secrets.token_urlsafe(32))" > /root/wordpress-admin-password'
sudo /opt/hipanel/bin/hipanel sites create -domain example.com -title "Example" -admin-user siteadmin -admin-email admin@example.com -admin-password-file /root/wordpress-admin-password
sudo rm -f /root/wordpress-admin-password
```

Add `-issue-cert -certbot-email admin@example.com` only after the domain's DNS
and ports 80/443 are ready.

## Inspect sites and TLS

Open **Sites**, select a domain, and review the site root, database, WordPress,
TLS, and operation state. The CLI inventory is:

```shell
sudo /opt/hipanel/bin/hipanel sites list
```

When the UI reports **TLS: no**, confirm public DNS and port reachability before
selecting **Issue HTTPS**. The site indicator reads active Nginx configuration;
the **Ops** view performs a deeper check of the certificate served locally,
including hostname, trust, validity, and expiry.

## Reset a WordPress administrator password

1. Select the site under **Sites**.
2. Select **Reset WP admin password**.
3. Confirm the WordPress username or email.
4. Wait for the operation to finish.
5. Store the generated password shown in the centered result dialog before
   closing it.

The Snotic panel administrator and a WordPress administrator are separate
accounts.

## Isolate an existing site

Preview which sites need per-site Unix/PHP isolation:

```shell
sudo /opt/hipanel/bin/hipanel sites isolate
```

Apply isolation to one exact domain only after reviewing the plan:

```shell
sudo /opt/hipanel/bin/hipanel sites isolate -domain example.com -apply -confirm example.com
```

## Delete a site

!!! danger
    Site deletion can remove the WordPress root, database and user, Nginx and
    PHP-FPM configuration, Unix account, certificate assets, and local backups.
    S3 backups are retained. Take and verify a current backup first.

The browser always displays a server-generated impact preview and requires the
exact domain to be typed before deletion.

For CLI deletion, preview first:

```shell
sudo /opt/hipanel/bin/hipanel sites delete -domain example.com -preview
```

Only add destructive flags that match the reviewed plan:

```shell
sudo /opt/hipanel/bin/hipanel sites delete -domain example.com -confirm example.com -delete-files -delete-local-backups
```
