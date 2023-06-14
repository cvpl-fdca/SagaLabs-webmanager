# SagaLabs

This is how you connect to FDCA's SagaLabs through a VPN connection.

## Red team

Lab 1: https://sl-p-uc1-lab1-pre-vpn.westeurope.cloudapp.azure.com/ \
Lab 2: https://sl-p-uc1-lab2-pre-vpn.westeurope.cloudapp.azure.com/ \
Lab 3: https://sl-p-uc1-lab3-pre-vpn.westeurope.cloudapp.azure.com/

## Blue team

Lab 1: https://sl-p-uc1-lab1-post-vpn.westeurope.cloudapp.azure.com/

The scoreboard for blue teaming can be found at: https://sagalabs.ctfd.io/ 

## Prerequisites

- Install OpenVPN3

- Windows/MAC: OpenVPN client, download here: https://openvpn.net/community-downloads/  
- Linux: OpenVPN client guide here: https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/

### Windows

1. Open the link above, for your lab
2. Here you will be met by a login prompt. Credentials will be given at the event.
3. Type your name/alias into the "new client" prompt and press add (please do not revoke or download other users certificates).   
4. Download your configuration file/certificate via. the download button and save it in an appropriate place.  
5. In OpenVPN create a new VPN connection, choose file and import/chose the file you downloaded in step 4, then press connect.  
6. You are done! You should now be able to see that you are connected, your VPN IP-Address (should be something like 10.8.0.x).

### Mac

1. Open the link above, for your lab
2. Here you will be met by a login prompt. Credentials will be given at the event.
3. Type your name/alias into the "new client" prompt and press add (please do not revoke or download other users certificates).   
4. Download your configuration file/certificate via. the download button and save it in an appropriate place.  
5. Realize that Mac sux, and download Linux instead.

### Linux

1. Open the link above, for your lab
2. Here you will be met by a login prompt. Credentials will be given at the event.
3. Type your name/alias into the "new client" prompt and press add (please do not revoke or download other users certificates).   
4. Download your configuration file/certificate via. the download button and save it the downloads folder.
5. Activating the VPN (CLI)

```bash
openvpn3 config-import --config ~/Downloads/<name>.ovpn
openvpn3 session-start --config ~/Downloads/<name>.ovpn
```
6. You are done! You should now be able to see that you are connected, your VPN IP-Address (should be something like 10.8.0.x).
7. Disconnecting the VPN (CLI)

```bash
openvpn3 session-manage --disconnect --config ~/Downloads/<name>.ovpn
```
#Credentials and Info

## Credentials for blue team

<details>
<summary>Blue team click here</summary>
  
Elastic: \
URL: https://fdca.kb.westeurope.azure.elastic-cloud.com:9243 \
Username: `BlueTeam` \
Password: `1mR9Mf9N8ZhtwxjGMkMB`

theHive: \
IP: `10.10.10.30:9000` \
Username: `TBA` \
Password: `TBA`

</details>

<details>
<summary>Red team click here</summary>

C2 server (SSH): \
IP: `Redacted. Spørg din underviser` \
Username: `SagaC2` \
Password: `vFz3fcMPsTgaQAQLZMhTdfnu0HfCICeuXtooqEwfck05CthX8XOlYq`

RedTeamTools (RDP): \
IP: `10.10.10.99` \
Username: `RedTeam` \
Password: `Password1234!`
</details>
