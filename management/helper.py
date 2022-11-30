import os
import json
import string
import shutil
import random
from datetime import datetime

from .CONSTANTS import (
    PATH_PRODUCT_TEMPLATE,
    PATH_PRODUCTS,
    PATH_ROOT,
)

def _getExactlyPath(targetURL, srcURL = PATH_ROOT):
    currentURL = os.path.join(__file__)
    while True:
        headTail = os.path.split(currentURL)
        currentURL = headTail[0]
        tail = headTail[1]
        if tail == srcURL:
            break
    return currentURL + os.sep + targetURL

def _importDataConfig(dataConfigUrl):
    url = _getExactlyPath(dataConfigUrl)
    try:
        with open(url, encoding='utf-8') as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        print('ERROR: FileNotFoundError')
        return False

def _removeAccents(inputStr):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in inputStr:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

def _initFolderName(category='', street='', acreage='', price=''):
    _dtString = datetime.now().strftime('%H%M%S%m%d%Y')
    _category = _removeAccents(category).translate({ord(c): None for c in string.whitespace}).lower()
    _streetName = _removeAccents(street).translate({ord(c): None for c in string.whitespace}).lower()
    _acreage = acreage
    _price = price
    return f'{_category}_{_streetName}_{_acreage}_{_price}_{_dtString}'

def _createFolder(targetUrl='', folderName=''):
    if not os.path.exists(targetUrl):
        os.mkdir(targetUrl)
    count = 0
    while True:
        _folder = f'{targetUrl}{os.sep}{folderName}'
        if not os.path.exists(_folder):
            os.mkdir(_folder)
            return _folder
        else:
            count += 1

def _copyImages(srcUrl = [], targetUrl = ''):
    count = 0
    result = []
    for image in srcUrl:
        imageName = f'{targetUrl.split(os.sep)[-1]}_{count}{os.path.splitext(image)[-1]}'
        count += 1
        imageUrl = f'{targetUrl}{os.sep}{imageName}'
        shutil.copy(image, imageUrl)
        result.append(imageUrl)
    return result

def _randomIcon(icons_str):
    index = random.randint(0, len(icons_str) - 1)
    return icons_str[index]

    pass
def _initItem(idProduct = str):
    with open(_getExactlyPath(PATH_PRODUCTS), 'r', encoding='utf8') as f:
        products = json.load(f)

    with open(_getExactlyPath(PATH_PRODUCT_TEMPLATE), 'r', encoding='utf8') as f:
        template = json.load(f)
    
    try:
        product = products[idProduct]
    except KeyError as e:
        print('Product not found')
        return None

    d_category = str(product['Category'])
    d_city = str(product['City'])
    d_district = str(product['District'])
    d_ward = str(product['Ward'])
    d_streetName = str(product['Street name'])
    d_buildingLine = str(product['Building line'])
    d_acreage = str(product['Acreage'])
    d_construction = str(product['Construction'])
    d_function = str(product['Function'])
    d_fuiture = str(product['Fuiture'])
    d_legal = str(product['Legal'])
    d_price = str(product['Price'])
    d_description = str(product['Description'])
    d_imageFolder = str(product['Folder path'])

    header = template['headers'][random.randint(0, len(template['headers']) - 1)]
    description = template['descriptions'][random.randint(0, len(template['descriptions']) - 1)]
    contact = template['contacts'][random.randint(0, len(template['contacts']) - 1)]
    hashtag = template['hashtag']

    header = header.replace(r'{icon}', '--')
    description = description.replace(r'{icon}', '--')
    
    header = header.replace(r'{category}', d_category)
    header = header.replace(r'{city}', d_city)
    header = header.replace(r'{district}', d_district)
    header = header.replace(r'{ward}', d_ward)
    header = header.replace(r'{streetName}', d_streetName)
    header = header.replace(r'{building_line}', d_buildingLine)
    header = header.replace(r'{acreage}', d_acreage)
    header = header.replace(r'{construction}', d_construction)
    header = header.replace(r'{function}', d_function)
    header = header.replace(r'{fuiture}', d_fuiture)
    header = header.replace(r'{legal}', d_legal)
    header = header.replace(r'{price}', d_price)
    header = header.replace(r'{description}', d_description)
    header = header.replace(r'{contact}', contact)

    description = description.replace(r'{category}', d_category)
    description = description.replace(r'{city}', d_city)
    description = description.replace(r'{district}', d_district)
    description = description.replace(r'{ward}', d_ward)
    description = description.replace(r'{streetName}', d_streetName)
    description = description.replace(r'{building_line}', d_buildingLine)
    description = description.replace(r'{acreage}', d_acreage)
    description = description.replace(r'{construction}', d_construction)
    description = description.replace(r'{function}', d_function)
    description = description.replace(r'{fuiture}', d_fuiture)
    description = description.replace(r'{legal}', d_legal)
    description = description.replace(r'{price}', d_price)
    description = description.replace(r'{description}', d_description)
    description = description.replace(r'{contact}', contact)
    description = header + '\n' + description

    imageFolder = d_imageFolder + '/images_for_sell'
    if os.path.exists(imageFolder):
        images = os.listdir(imageFolder)
        imagesTemp = []
        imagesTemp2 = []
        
        for image in images:
            imagesTemp.append(imageFolder + '/' + image)

        if len(imagesTemp) >= 6:
            while len(imagesTemp2) < 6:
                i = random.randint(0, len(imagesTemp) - 1)
                if imagesTemp2.count(imagesTemp[i]) == 0:
                    imagesTemp2.append(imagesTemp[i])
            images = '\n'.join(imagesTemp2)
        else:
            images = '\n'.join(imagesTemp)
    else:
        os.mkdir(imageFolder)    
        images = ''
    
    return {
        'header': header,
        'district': d_district,
        'description': description,
        'hashtag': hashtag,
        'images': images,
    }