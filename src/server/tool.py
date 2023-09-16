def get_file_size(content_length):

    size = content_length
    if(not isinstance(content_length,int)):
        # Convert the content length to integer
        size = int(content_length)

    # Define the units
    units = ['bytes', 'KB', 'MB']

    # Iterate through the units and divide the size by 1024
    for unit in units:
        if size < 1024:
            # Return the file size and unit
            return f"{size:.2f} {unit}"
        size /= 1024

    # If the size is larger than the last unit, return in GB
    return f"{size:.2f} GB"
