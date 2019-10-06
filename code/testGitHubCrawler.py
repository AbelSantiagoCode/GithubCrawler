import unittest
from gitHubCrawler import GitHubCrawler



class TestCrawler(unittest.TestCase):
    """docstring for TestCrawler.
    command exucution: python3 -m unittest -v testGitHubCrawler
    """
    def setUp(self):
        self.Crawler = GitHubCrawler(["openstack","nova","css"],"5.196.132.118:3128")

    def test_Repositories(self):
        result = self.Crawler.getLinksRepos()
        if result == []:
            self.assertEqual(result,[])
        else:
            self.assertEqual(result,['https://github.com/atuldjadhav/DropBox-Cloud-Storage', 'https://github.com/michealbalogun/Horizon-dashboard'])

    def test_Issues(self):
        result = self.Crawler.getLinksIssues()
        if result == []:
            self.assertEqual(result,[])
        else:
            self.assertEqual(result,['https://github.com/novnc/websockify/issues/180', 'https://github.com/altai/nova-billing/issues/1', 'https://github.com/rclone/rclone/issues/2713', 'https://github.com/sfPPP/openstack-note/issues/8', 'https://github.com/hellowj/blog/issues/37', 'https://github.com/bblfsh/python-driver/issues/202', 'https://github.com/moby/moby/issues/19758', 'https://github.com/YumaInaura/YumaInaura/issues/1322', 'https://github.com/jupyterhub/the-littlest-jupyterhub/issues/108', 'https://github.com/aaronkurtz/gourmand/pull/35'])

    def test_Wikis(self):
        result = self.Crawler.getLinksWikis()
        if result == []:
            self.assertEqual(result,[])
        else:
            self.assertEqual(result,['https://github.com/vault-team/vault-website/wiki/Quick-installation-guide', 'https://github.com/iwazirijr/wiki_learn/wiki/Packstack', 'https://github.com/marcosaletta/Juno-CentOS7-Guide/wiki/2.-Controller-and-Network-Node-Installation', 'https://github.com/MirantisDellCrowbar/crowbar/wiki/Release-notes', 'https://github.com/dellcloudedge/crowbar/wiki/Release-notes', 'https://github.com/eryeru12/crowbar/wiki/Release-notes', 'https://github.com/jamestyj/crowbar/wiki/Release-notes', 'https://github.com/rhafer/crowbar/wiki/Release-notes', 'https://github.com/vinayakponangi/crowbar/wiki/Release-notes', 'https://github.com/kingzone/node/wiki/Modules'])

    def test_LanguageStatRepos(self):
        result = self.Crawler.getLangStatRepos("https://github.com/atuldjadhav/DropBox-Cloud-Storage")
        if result == {}:
            self.assertEqual(result,{})
        else:
            self.assertEqual(result,['atuldjadhav', {u'JavaScript': u'47.2', u'HTML': u'0.8', u'CSS': u'52.0'}])


if __name__ == '__main__':
    unittest.main()
