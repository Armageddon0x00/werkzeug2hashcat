#!/usr/bin/env python3
import base64
import codecs
import re
import argparse

# Thanks https://github.com/hashcat/hashcat/issues/3205#issuecomment-2415236705

def process_hash(example):
    m = re.match(br'pbkdf2:sha256:(\d*)\$([^\$]*)\$(.*)', example)
    if not m:
      print("Invalid hash format. Check for weird characters if you are supplying the hash directly from terminal.")
      return None
    
    iterations = m.group(1)
    salt = m.group(2)
    main_hash = m.group(3)
    
    decoded_hash = codecs.decode(main_hash, 'hex')

    return f"sha256:{iterations.decode()}:{base64.b64encode(salt).decode()}:{base64.b64encode(decoded_hash).decode()}"

def main():
    parser = argparse.ArgumentParser(description="Process PBKDF2 hash(es) from input and convert to applicable hashcat format.")
    parser.add_argument('-s', '--hash', type=str, help="Single PBKDF2 Werkzeug hash to process.")
    parser.add_argument('-l', '--hashlist', type=str, help="File containing PBKDF2 Werkzeug hashes to process, one per line.")
    
    args = parser.parse_args()

    if args.hash:
      hashcat_hash = process_hash(args.hash.encode())
      print(hashcat_hash)
      print(f"You can now crack this hash using: hashcat -m 10900 {hashcat_hash} /usr/share/wordlists/rockyou.txt")
    elif args.hashlist:
      hashlist = []
      try:
        with open(args.hashlist, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                  hashcat_hash = process_hash(line.encode())
                  hashlist.append(hashcat_hash)
                  print(hashcat_hash)
        with open('werkzeug_converted_hashcat.hash', 'w') as hashout:
            for hashcat in hashlist:
              hashout.write(hashcat + "\n")
        print(f"You can now crack this hashes using: hashcat -m 10900 werkzeug_converted_hashcat.hash /usr/share/wordlists/rockyou.txt")

      except FileNotFoundError:
          print(f"File {args.hashlist} not found.")
    else:
      print("Please provide either a single hash (-s) or a file containing hash each line (-l).")

if __name__ == '__main__':
  main()