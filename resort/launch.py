import options
import etalons

from basic_rest_def import PingEntry


def basic_etalon_saving_example():
    opts = options.read_all()
    ping_entry = PingEntry(opts['input'])
    response = ping_entry.read()
    etalon = etalons.BasicHTTPResponseEtalon(response)
    eio = etalons.EtalonIO(opts)
    eio.save(etalon, opts.get('output'))


if __name__ == '__main__':
    basic_etalon_saving_example()
