import olefile
import binascii

# Path to the uploaded file
file_path = 'tournament-files/2022 Chicago Open/U1000-34.S2C'

# Open the file and read its contents
with open(file_path, 'rb') as f:
    data = f.read()

# Print the first few bytes as hex for inspection
print("Hexadecimal content (first 200 bytes):")
print(data[:200].hex())

# Try interpreting the file as an OLE compound file
if olefile.isOleFile(file_path):
    print("\nThe file is recognized as an OLE compound file.")

    # Open the OLE file
    ole = olefile.OleFileIO(file_path)

    # List all the streams and storages in the file
    print("\nStreams and Storages in the file:")
    streams = ole.listdir()
    for stream in streams:
        print("/".join(stream))

    # Example: Read and display the 'Workbook' stream if it exists
    if ole.exists('Workbook'):
        stream = ole.openstream('Workbook')
        workbook_data = stream.read()
        print("\nWorkbook stream content (first 200 bytes):")
        data = workbook_data[200:]
        result_string = data.strip().decode('utf-8')
        print(result_string)
        # isdecoded_data = binascii.unhexlify(data)

        # print(workbook_data[:200].hex())  # Display as hex

        # Further processing of the workbook_data can be done here



    # Check for any other interesting streams
    other_streams = ['\x05SummaryInformation', '\x05DocumentSummaryInformation']
    for s in other_streams:
        if ole.exists(s):
            stream = ole.openstream(s)
            summary_data = stream.read()
            print(f"\nContent of {s} (first 200 bytes):")
            print(summary_data[:200].hex())

    ole.close()
else:
    print("\nThe file does not appear to be a standard OLE compound file.")

# You can add more specific parsing and extraction logic depending on what you find in the streams.
