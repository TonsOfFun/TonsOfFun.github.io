---
layout: about
title: Justin Bowen is TonsOfFun
description: Born and raise on the peninsula in the San Francisco, I was fortunate to be exposed to both business and technology at a very young age. Video games were a huge influence on my interest in computers and programming. I used to play games like DOOM, Quake, Hexen, and Duke Nukem 3D at my dad's office with the tech support crew at the end of the work day. 
---
# <%= resource.data.title %>
{: .text-4xl.font-bold.tracking-tight.text-zinc-800.dark:text-zinc-100.sm:text-5xl }

<%= collections.posts.resources.select! {|resource| resource.relative_url.split('/').last == 'about' }.first.content %>