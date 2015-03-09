from __future__ import print_function
import pygraphviz as pgv


def vizTree(tree):
    graph = pgv.AGraph(directed=True, rankdir="LR")

    def walk(node, parent=None, dist=None):
        if parent:
            graph.add_edge(
                parent,
                node["string"],
                label=dist
            )
        for key in node["children"]:
            walk(node["children"][key], parent=node["string"], dist=key)

    walk(tree._tree)

    print(graph)


if __name__ == "__main__":
    from bktree import BKTree
    from hamdist import hamdist

    tree = BKTree(hamdist)

    for word in [
        "47c70418f7e8bffffcf27e3eee665e1cf0f8f83010006eff",
        "228c301669d2bfff8403878f0d48981dff9901410000efff",
        "f18b152a16ecb37ffffd3c7c7c3c0cac38f8f8f0703020ff",
        "833df3ce0953beff2622323030367676006063461e0cffff",
        "130214ed03f4ff7fd4fcf8f8f060b9b9fc3c80c00000f0ff",
        "3f03cc291fe4fdfff6a0a0425a5bdbdbfedf8c0030107cff",
        "9e012cd0eb06b0ff84032333339393d3efcfc1c0583f00ff",
        "070f38f68d6abfff34c8c8c8d87e7e3ff0e8030307107cff",
        "1ce01183e4c3bfffc44d6d656131b191100e0f3301093fff",
        "ff1e63cc31ebd7efe4babaf83939b9cb848fc7c2c0e0f3ff",
        "8c31c70011c0bfffc42941092d6773c33fc7c70000007fff",
        "c8137f38c3d8bf7fd4b59494c4e4e66670f0e08e03007fff",
        "80047d8111c3bfff44ad2d292929392e3f0981070000ffff",
        "feb863c70f48bfff846171dd892125250f0f0f060f047fff",
        "f180a3070fecbcffdcfdfdfdfdfdfdfd3c3c3c3c180078ff",
        "f9b3479e0870eafff6fdfdd8d0f0e4e4007c7c7c7c4400ff",
        "39c77af38d71aefff743435159595959000c002557ce7fff",
        "8225dab0c37fa3ff240181c60636363effe3c18103705cff",
        "3ef48631c7ccbfff54d694b5b5b1f9e9401c1e1a1301ffff",
        "ed70fbf60360bfff7cdf8999d125a5a50020060f8f04ffff",
        "01ee9d776fcebdff84cace8e8cccaeec000000101938ffff",
        "193274c20ec1bffff4e2e26272f2e0f2e6e6262600001cff",
        "1e31408813e2ffff440383c343535353f7c787808080e0ff",
        "131cb3c2a1c1bfff0060f2fa7a3d070fc403c34301000fff",
        "7ef1c208f1eeffff848303c7c7c3436302078f880000feff",
        "40fc13479ce3ffffdc73b5fced2d8d2d00003832e008ffff",
        "e913c71813e4fffffcfdf9e9e9e4e0c00cf0c4080000ffff",
        "00fcfb4700e0ffff4498193be7c783831c00063f0f00feff",
        "f0c387670ff8fc7ff4fcfcfcdc5cdcdc303838187c3838ff",
        "d160c3071fc0bffff7f96961313139b91c0c0c1c1c007fff",
        "e85bd1070f36b8ffffd4d4c4fcfc8c8c70381e1f3e1808ff",
        "80b137ee80c8bfffcc2d2565f78783e33f0670623000ffff",
        "f0c13f9608c1bffffc393d3d3dbdfddd1c3c7c670301c9ff",
        "06fc10b26cd3adff000b0b2f2b0b0b0b8b83832381c9c3ff",
        "ba655bf490efbe7f0081e1f53131151400046c878783fbff",
        "ed1bc7e4bd53a67ff7fcdcdcecccc4c5183866024e4fcfff",
        "030f760810effe7f44c49c3c7a7a5a5af8cdc3c60008f8ff",
        "70ce3143aef1fffffdb9f9f9f9d9d9f90c1c1e0323c0e3ff",
        "dd230708bce2fffff6f67675f535f4f4647e70100000ffff",
        "c177fed0ed9bbffffc89a9b9d956d6561840400f0f07ffff",
        "99b3455ae6c5bfffdc687070f1703071b864242000027fff",
        "72c108209cf1ffff3c020b0b4b0bd8fcfffff9000000fcff",
        "52a47df30fd0bffff0a93931131b2b2b0c0da1103f007fff",
        "050320c643ddf7fffc7db494f92086af7c7a00400020ffff",
        "00ffe70f18eeb77fcbdb52525a5858120000787cfc787fff",
        "fefdf3872dc2bffff459555565e50d1900003f3f1d0f0fff",
        "870830e811e3bf7fc48cac6c26860686fb63230000007fff",
        "00f5ff0c04faff7f19b1b5d0d1d5d2570440780e2440ffff",
        "934c738f66c0ff7f5461616171b9bdbf0408437438047eff",
        "41f73c7b84c8bfffdceefeba7a5252e4000038b62703ffff",
        "01c6083045c0bfffdcfcfcfcf8fcd87cfc5819080000ffff",
        "330f9ebc79c2b7ffd0ede41c1c5a585a7cd9c1c1c9c963ff",
        "1fb2a10244c1bffff4f9f1e1e1e1c1411c0e0f07010077ff",
        "280044e91e7fbfff1c9783cbcbc3c1f0ffd7000000607cff",
        "71c2946f1fe0bf7fdc9f5d5969d9d8fd5a1800004200ffff",
        "410227cd0ce9ba7ffedcd8fc6c6c6c7ef8f060703c187eff",
        "03e2f50811ccbfff12088a9a7abababa0080e07c1c007fff",
        "1e1780f1c503beff441d0d01dbdbda5bffdf87000b0600ff",
        "30c243b20ceebffffcf97979f9f9d9c90c1e1a000000fdff",
        "6103a77f3ffcc10fdcf3c3c38acede9e0600c0f0f0f0f8ff",
        "ee0ddb039f7d9bfffcdd945565e5ed9d1030010c74f47eff",
        "03c0217eb0c1ff7f140000223e9b894bff8330c08100c1ff",
        "ed9b110e20fddf7fd6cdcdcd4d0d8d091a3e1e0201e0f1ff",
        "c1031c3976fcc3ffd4e8c8d096366e6efef8800081e1e1ff",
        "038e18eb90e3dfff001878d8eefe2a2efdc1e1f0808000ff",
        "7b93468913e4b9fffc5c5c7878f8f97978fcde06381010ff",
        "05fc83c716e0bf7f748c0c8c0e1e1dd930000e141e00ffff",
        "9df1075f20f8ff7fff4114c5c7d7f53562663e70240026ff",
        "f78f1fa018e0c33f7c71d0fce8ececce0038fbe3c1c080ff",
        "ce0176ecd13dc0ff7aede565656767433ff7c1c1c0e80010",
        "0e5130f0e1d5bfff14131333d3c3c3c3c7c7c3010103ffff",
        "e2c33c079ee0b9fff4f1f17d3c1c8cc41c7830f170301cff",
        "816fb6b1cc3cab7ffcede4e6f2b2121a34c0c32321f3f5ff",
        "056b14eb8081bf7fdc5e561716161634424008060602ffff",
        "01cecf3d72e4ffff7cdefaf8d8fedc9c000000b89880ffff",
        "b8f933870dc0bffff4b535b1b1b1f1d500003e3e7d007eff",
        "1172f98f1448bfffff97b53323a383ab260201ef2e0010ff",
        "9b4b941fe288bffffcf4f4e4e47c9c1c203098f8380e1fff",
        "6c749a93e5a2ff7f701b49250383c14a03078d030102e6ff",
        "40833ce800c0bfff7e5cfcfcfc687040f9fcf0e2c10000ff",
        "c1176bc607c0bf7fdcfdfc7c646464e5383420263c003cff",
        "a234ea0083e3ffff0435351d2d7d6df928100c0e0604ffff",
        "1e1ce3a74bc0bf7fd40387862a5df5a50000022110007fff",
        "050fbcc813e0fffff492424262eea68ef2e2c1c39000faff",
        "ea06a853ee8bb5ff048bcb68acececad9bbd0111210f0fff",
        "479e289933e4da7f442c2c2e6e6e6e6eb191b1919880e0ff",
        "0107668fdce0fffffefcfcfc7c78da5af8c8c0606000ffff",
        "dc7f8661e3979ffffded6d65713171d0000cce03118f9fff",
        "f8c08931e29ebbfffdf1e1a181d9f9f93e3e3e19011314ff",
        "18b0612649d1ffff004303030343236307070606c341efff",
        "1db207cbb041bffffea2a3a7c7c52121e6069ce0000079ff",
        "110a3c9ff8f007ffc4e666623a269e9c000000e1f1c3cfff",
        "fd0f478010f9bf7ffdddbdbdbcbcb1b1183cee4c04003cff",
        "0d02982cf083fffffec6c6c64e6a9a9af2fa40000000feff",
        "1ff0c0171ef0cfff000aca4b0343430181071e3c78c0f8ff",
        "e1fe470b0ef0ebfffcfcacac2c6ce8c80010387c7c5074ff",
        "689022c523ffbfffecc14159c1c1e1e11e1e16041c007eff",
        "b067ceb003ebffff552de5d5d89818181e484c0d0d087eff",
        "234fa6c83941beffd49a9adada7a5adac0c0c0000c0c4dff",
        "c73f778c69d1afff4e16cec6ce46262600e0e3434040d7ff"
    ]:
        tree.insert(word)

    vizTree(tree)
