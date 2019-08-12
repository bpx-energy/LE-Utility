def ClearCombobox(item):
    item.blockSignals(True)
    item.clear()
    item.addItem('--')
    item.blockSignals(False)

