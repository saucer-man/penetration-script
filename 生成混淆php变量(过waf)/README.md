过waf？直接出现关键词肯定是不行滴

但是怎么混淆呢？亦或就行了。

```php
<?php
$_fmE="*"^"\x4f";//e
$_nbt="J"^"\x3c";//v
$_iSu="["^"\x3a";//a
$_qjD="K"^"\x27";//l

$target=$_fmE.$_nbt.$_iSu.$_qjD;
print_r(target) //eval
?>
```

批量生成？

![result](result.png)