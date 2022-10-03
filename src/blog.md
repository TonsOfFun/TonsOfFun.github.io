---
layout: page
title: Posts
---
<header class="max-w-2xl">
  <h1 class="text-4xl font-bold tracking-tight text-zinc-800 dark:text-zinc-100 sm:text-5xl">Writing on
    software design, company building, and the aerospace industry.</h1>
  <p class="mt-6 text-base text-zinc-600 dark:text-zinc-400">All of my long-form thoughts on
    programming, leadership, product design, and more, collected in chronological order.</p>
</header>
<div class="mt-16 sm:mt-20">
  <div class="md:border-l md:border-zinc-100 md:pl-6 md:dark:border-zinc-700/40">
    <div class="flex max-w-3xl flex-col space-y-16">
      <% collections.posts.resources.each do |post| %>
        <% unless post.data.draft %>
          <%= render ArticleCard.new(article: post) %>
        <% end %>
      <% end %>
    </div>
  </div>
</div>
<!-- If you have a lot of posts, you may want to consider adding [pagination](https://www.bridgetownrb.com/docs/content/pagination)! -->
