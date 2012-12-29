from pickle import dump, load
from operator import itemgetter

class Color(object):
    """A color of DMC floss.

    Has a String name and RGB hex value.
    """
    
    def __init__(self, name, rgb):
        self.name = name
        self.rgb = int(rgb, 16)

    @property
    def red(self):
        """Get the red component of the RGB value."""
        return self.rgb // (256 ** 2)

    @property
    def green(self):
        """Get the green component of the RGB value."""
        return (self.rgb // 256) % 256

    @property
    def blue(self):
        """Get the blue component of the RGB value."""
        return self.rgb % 256

    def __str__(self):
        return 'Color(' + self.name + ', ' + hex(self.rgb) + ')'

def search(pantone, top=10):
    """Search for the top TOP floss colors closest to the Pantone color
    specified by the string PANTONE.
    """
    #Search for Pantone color
    p_color = None
    for color in pantone_colors:
        if color.name.lower() == pantone.lower():
            p_color = color

    #If search failed, return.
    if not p_color:
        print("Could not identify Pantone color.")
        return

    #Calculate closeness of DMC colors and construct dictionary with values
    matches = {}
    for d_color in dmc_colors:
        #Calculate distance
        rdist = p_color.red - d_color.red
        gdist = p_color.green - d_color.green
        bdist = p_color.blue - d_color.blue
        dist = rdist**2 + gdist**2 + bdist**2

        #Add to dictionary
        matches[d_color.name] = dist

    #Sort dictionary
    sorted_matches = sorted(matches.items(), key=itemgetter(1))
    for match in sorted_matches[:10]:
        print(match[0])

def pickle_pantone():
    """Extract Pantone/RGB pairs from text and pickle them.
    """
    pantone_file = open('Pantone to RGB.txt')
    colors = [] #All Pantone colors

    #Get non-blank lines
    lines = (line.rstrip() for line in pantone_file.readlines())
    lines = (line for line in lines if line)
    
    #Load all colors into array
    for line in lines:
        #Process line
        split_line = line.split()
        rgb = split_line[-1] #RGB val is last word
        rgb = rgb[1:] #Remove pound character
        name = ' '.join(split_line[:-1]) #Name is rest of line

        #Add color
        color = Color(name, rgb)
        colors.append(color)

    #Pickle array
    dump(colors, open('PantoneColors.p', 'wb'))

def pickle_dmc():
    """Extract DMC/RGB pairs from text and pickle them.
    """

    dmc_file = open('DMC to RGB.txt')
    colors = [] #All DMC colors

    #Load all colors into array
    for line in dmc_file.readlines():
        split_line = line.split()
        color = Color(split_line[0], split_line[1])
        colors.append(color)

    #Pickle array
    dump(colors, open('DMCColors.p', 'wb'))

pantone_colors = load(open('PantoneColors.p', 'rb'))
dmc_colors = load(open('DMCColors.p', 'rb'))
