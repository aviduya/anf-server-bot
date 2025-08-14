from smtpd import usage
from urllib import response
from config import SERVER_URL, SERVER_TOKEN
import httpx
import logging


log = logging.getLogger(__name__)

async def command(interaction, command: str, directive=None):
    user = interaction.user
    log.usage(f"{user} invoked /{command}")
    token = SERVER_TOKEN
    url = f"{SERVER_URL}/command"

    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
    }

    payload = {
        "command": f"{command} {directive}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            await interaction.response.send_message(
                f"Command sent to server: {command} {directive}",
                ephemeral=True
            )
            log.usage(f"{command} {directive} completed by {user}")

    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        await interaction.response.send_message("Failed to send message to server.", ephemeral=True)
    except httpx.RequestError as e:
         log.error(f"Request error: {e}")
         await interaction.response.send_message("Connection error occurred.", ephemeral=True)



 # async def say(interaction, message: str):
 #     user = interaction.user
 #     log.usage(f"{user}: invoked /say")
 #     URL = f"{url}/command"

 #     headers = {
 #         "Authorization": f"Bearer {token}",
 #         "Content-Type": "application/json"
 #     }

 #     payload = {
 #         "command": f"say {user}: {message}"
 #     }

 #     try:
 #         async with httpx.AsyncClient() as client:
 #             response = await client.post(URL,
 #                 json=payload,
 #                 headers=headers)
 #             response.raise_for_status()

 #             await interaction.response.send_message(
 #                 f"Message sent to server: {message}",
 #                 ephemeral=True
 #             )
 #         log.usage(f"{user}: {message}")
 #     except httpx.HTTPStatusError as e:
 #         log.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
 #         await interaction.response.send_message("Failed to send message to server.", ephemeral=True)
 #     except httpx.RequestError as e:
 #         log.error(f"Request error: {e}")
 #         await interaction.response.send_message("Connection error occurred.", ephemeral=True)
