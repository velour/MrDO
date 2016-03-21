import digitalocean

keyFile = open("./config/digital-ocean-test-key")
secretKey = keyFile.read()
secretKey = secretKey.strip()

manager = digitalocean.Manager(token=secretKey)


def get_image_by_name(manager, name):
    """
    Manager is a digitalocean.Manager
    name is the name of an image

    if the image exists, start a droplet based on that image
    if there are more than a single image with the same name in the list, the fail
    """
    images = manager.get_my_images()
    toRet = None
    for image in images:
        if image.name == name:
            if toRet:
                raise Exception("get_image_by_name: There are two images with the same name!")
            else:
                toRet = image
    if toRet:
        return toRet
    else:
        raise Exception("get_image_by_name: There was no such image in images")


def more_recent(image1, image2):
    """
    true if image1 is more recent than image 2, according to image.created_at
    """
    if image1.created_at > image2.created_at:
        return -1
    elif image1.created_at < image2.created_at:
        return 1
    else:
        return 0


def get_most_recent_image(manager):
    """
    Manager is a digitalocean.Manager

    if there are no images, the fail
    otherwise, return the most recent image by time

    if two images have the same time exactly, that's really surprising. also fail.
    """
    ## created_at gives the images time
    images = manager.get_my_images()
    if images:
        if len(images) == 1:
            return images[0]
        else:
            sortImages = sorted(images, cmp = more_recent)
            mostRecent = sortImages[0]
            maybeAsRecent = sortImages[1]
            if(maybeAsRecent.created_at == mostRecent.created_at):
                raise "start_most_recent_image: Most recent is ill defined!"
            else:
                return mostRecent
    else: ## there are no images.
        raise "start_most_recent_image: There is no most recent image!"


def droplet_of_image(imagedict):
    """
    Spin up a droplet from the specified image

    Note that the droplet hasn't been constructed yet, you have to create it and
    destroy it by hand
    """
    imagedict.load() ## just in case we haven't yet, but I don't know that this has any effect for us?
    droplet = digitalocean.Droplet(
        token=secretKey,
        name = imagedict.name,
        image = imagedict.id,
        region = 'nyc2', ## this should be pulled from the imagedict [JTT 21-03-16]
        size = '4GB',    ## this should be pulled from the imagedict
        backups = False)
    return droplet


def snapshot_droplet(droplet, name):
    """
    Save a snapshot of the droplet
    """
    raise Exception("stub")


def tearDown(droplet, name=None):
    """
    For a running droplet, take a snapshot, then destroy the active droplet.
    """
    if name == None:
        name = droplet.name ## and append some sort of UID, time stamp, something
    droplet.power_off()
    snapshot_droplet(droplet, name)
    droplet.destroy()
