BitTorrent
==========

### In-Browser BitTorrent

<quote><cite>...in practice it turned out to not be such a good idea, because of the severe impact it had on the browser, so we moved on to outboard bittorrent clients like Red Swoosh and BitTorrent DNA, which are easy to integrate with the browser via http.

Making the web browser grow much larger, and keeping it constantly busy doing lots of extra network and disk io, and increasing the code complexity and risk it might crash, is just not a good idea in general. Separating the bittorrent client out into its own process that doesn't have any impact on the browser and can be shared by other applications, and communicating with it via http (one data channel and one control channel -- and no plugins) was a much cleaner and more robust solution.</cite><span>— <author>Hopkins, Don</author>, <book><a href='http://www.reddit.com/r/programming/comments/2g7yqf/webtorrent_is_a_streaming_torrent_client_that/'>WebTorrent Is A Streaming Torrent Client</a></book></span></quote>

