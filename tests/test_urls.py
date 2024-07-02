def test_blog_urls():
    try:
        from blog.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'При импорте списка маршрутов `urlpatterns` из файла '
            f'`blog/urls.py` произошла ошибка: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Убедитесь, что значением переменной `urlpatterns` является список.'
    )
    assert len(solution_urlpatterns) >= 3, (
        'Убедитесь, что к головному списку `urlpatterns` подключены маршруты '
        'из файла `blog/urls.py`.'
    )


def test_pages_urls():
    try:
        from pages.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'При импорте списка маршрутов `urlpatterns` из файла '
            f'`pages/urls.py` произошла ошибка: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Убедитесь, что значением переменной `urlpatterns` из файла '
        '`pages/urls.py` является список.'
    )
    assert len(solution_urlpatterns) >= 2, (
        'Убедитесь, что к головному списку `urlpatterns` подключены маршруты '
        'из файла `pages/urls.py`.'
    )


def test_blogicum_urls():
    try:
        from blogicum.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'При импорте списка маршрутов `urlpatterns` из файла '
            f'`blogicum/urls.py` произошла ошибка: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Убедитесь, что значением переменной `urlpatterns` из файла '
        '`blogicum/urls.py` является список.'
    )
    assert len(solution_urlpatterns) >= 3, (
        'Убедитесь, что к головному списку `urlpatterns` подключены маршруты '
        'из файла `blogicum/urls.py`.'
    )
