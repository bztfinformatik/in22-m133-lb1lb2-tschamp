function deleteProduct(element) {
    if(window.confirm("Wollen Sie das Item wirklich löschen"))
    {
        element.parentElement.submit();
    }
}

