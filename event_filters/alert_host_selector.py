import dpath

import multiprocessing as mp

def clean_host(host):
    if ":" in host:
        return host.split(":")[0]
    else:
        return host

def main(event):
    logger = mp.get_logger()
    try:
        host = dpath.util.get(event, 'alert.labels.instance', separator=".")
        host = clean_host(host)
        if host is not None:
            event['meta']['hosts'] = [host]
            logger.info(event)
    except KeyError:
        pass
    return event
