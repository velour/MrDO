import digitalocean

keyFile = open("./config/digital-ocean-test-key")
secretKey = keyFile.read()
secretKey = secretKey.strip()

manager = digitalocean.Manager(token=secretKey)


def get_image_by_name(manager, name):
    """
    Manager is a digitalocean.Manager
    name is the name of an image

    if the image exists, return it.
    if no image by that name exists, return an error saying that.
    if more than a single image with that name exists, return an error.
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
    compares created_at of two images. When used as part of sorted or
    list.sort, returns a list from most to least recent according to
    the creation date of the image.
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

    if two images have the same time exactly, that's really
    surprising. also fail.
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

    if a droplet of that name exists, fail
    """
    raise Exception("stub")


def tearDown(droplet, name=None):
    """
    For a running droplet, take a snapshot, then destroy the active droplet.
    returns the name of the constructed snapshot

    The standard approach to snapshotting a droplet for later use is:
      power the droplet off
      ask DigitalOcean to take a snapshot
      wait until the snapshot is constructed
      destroy the droplet so you stop paying for it
    """
    if name == None:
        name = droplet.name ## append some sort of UID, time stamp, etc
    droplet.power_off()
    snap_name = snapshot_droplet(droplet, name)
    droplet.destroy()
    return snap_name
