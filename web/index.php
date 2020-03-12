<?
	if (isset($_GET["path"])){
		header("Location: https://github.com/cache-sk/kodirepo/raw/master/repository/repository.cache-sk/".$_GET["path"]);
		die;
	}
	$contents = file_get_contents("https://github.com/cache-sk/kodirepo/tree/master/repository/repository.cache-sk");
	preg_match_all('/.*title="repository.cache-sk-([0-9]+.[0-9]+.[0-9]+).zip".*/', $contents, $matches);
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
<body>
<a href="repository.cache-sk-<?=$matches[1][0]?>.zip">repository.cache-sk-<?=$matches[1][0]?>.zip</a>
</body>
</html>