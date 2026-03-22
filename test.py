import subprocess, json, os
from pprint import pprint
os.makedirs("logs", exist_ok=True)

subprocess.run(
    ["suricata", "-r", "data/2020-10-29-Hancitor-infection-with-Cobalt-Strike.pcap", "-l", "logs", "-k", "none"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

output = []

with open("logs/eve.json") as f:
    for line in f:
        d = json.loads(line)
        pprint(d)
        # if d.get("event_type") in ["dns", "alert"]:
        #     output.append({
        #         "timestamp": d.get("timestamp"),
        #         "src_ip": d.get("src_ip"),
        #         "dst_ip": d.get("dest_ip"),
        #         "src_port": d.get("src_port"),
        #         "dst_port": d.get("dest_port"),
        #         "protocol": d.get("proto"),
        #         "app_proto": d.get("app_proto"),
        #         "flagged": d.get("event_type") == "alert",
        #         "alerts": [{
        #             "signature": d["alert"].get("signature"),
        #             "severity": d["alert"].get("severity")
        #         }] if d.get("event_type") == "alert" else []
        #     })

# print(json.dumps(output[:5], indent=4))