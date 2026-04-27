{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block html %}
This is an <strong>html</strong> message.

<img src='https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fwww.mamp.one%2Ffree-image-resources-for-web-designers-where-to-find-high-quality-visuals%2F&ved=0CBYQjRxqFwoTCPCI8eXcjpQDFQAAAAAdAAAAABBu&opi=89978449'>
{% endblock %}