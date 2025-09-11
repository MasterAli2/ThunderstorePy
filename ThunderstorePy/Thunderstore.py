from typing import Dict
import uuid
import requests

class PackageList:
    _packages: list['PackageListing']
    _full_name_map: Dict[str, 'PackageListing']

    def __init__(self):
        self._packages = []
        self._full_name_map = {}
        
    def add_package(self, package: 'PackageListing') -> None:
        self._packages.append(package)
        self._full_name_map[package.full_name] = package

    def get_package_by_uuid(self, uuid4: str) -> 'PackageListing':
        return self._full_name_map.get(uuid4)

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice): 
            return self._packages[key]
        elif isinstance(key, str): 
            return self._full_name_map[key]
        else:
            raise TypeError("Key must be int, UUID (string), or slice")

    def __iter__(self):
        yield from self._packages

class PackageListing:
    name: str = None
    full_name: str = None
    owner: str = None
    package_url: str = None
    donation_link: str = None
    date_created: str = None
    date_updated: str = None
    uuid4: str = None
    rating_score: str = None
    is_pinned: str = None
    is_deprecated: str = None
    has_nsfw_content: bool = None
    categories: str = None
    versions: list['PackageVersion'] = None

class PackageVersion:
    name: str = None
    full_name: str = None
    description: str = None
    icon: str = None
    version_number: str = None
    dependencies: list[str] = None
    download_url: str = None
    downloads: int = None
    date_created: str = None
    website_url: str = None
    is_active: bool = None
    uuid4: str = None

class PackageMetrics:
    downloads: int = None
    rating_score: int = None
    latest_version: str = None

class PackageVersionMetrics:
    downloads: int = None

def FromJson(obj, data):
    for i in obj.__annotations__:
        if (i in data):
            setattr(obj, i, data[i])
    return obj

def getPackageList(community :str) -> PackageList:
    r = requests.get(url=f"https://thunderstore.io/c/{community}/api/v1/package/")
    r.raise_for_status()
    packageList: PackageList = PackageList()
    data = r.json()
    for package_data in data:
        packageList.add_package(FromJson(PackageListing(), package_data))
    for package in packageList:
        package.versions = [FromJson(PackageVersion(), v) for v in package.versions]
    return packageList

def getPackageMetrics(namespace: str, name: str) -> PackageMetrics:
    r = requests.get(url=f"https://thunderstore.io/api/v1/package-metrics/{namespace}/{name}/")
    r.raise_for_status()
    return FromJson(PackageMetrics(), r.json())

def getPackageVersionMetrics(namespace: str, name: str, version:str) -> PackageVersionMetrics:
    r = requests.get(url=f"https://thunderstore.io/api/v1/package-metrics/{namespace}/{name}/{version}/")
    r.raise_for_status()
    return FromJson(PackageVersionMetrics(), r.json())

if __name__ == "__main__":
    a = getPackageList("content-warning")
    print(a[a[865].uuid4])