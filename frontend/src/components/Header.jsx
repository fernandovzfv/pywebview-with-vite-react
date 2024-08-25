import { Flex, Text, Link } from "@radix-ui/themes";
import Ticker from "./Ticker";
import logo from "../assets/logo.png";

export default function Header() {
  return (
    <Flex
      align="center"
      justify="between"
      px="4"
      py="2"
      style={{ backgroundColor: "var(--gray-8)" }}
    >
      <Flex align="center" gap="4">
        <img src={logo} alt="Logo" width="32" height="32" />
        <Text size="5" weight="bold">
          pywebview
        </Text>
        <Ticker />
      </Flex>
      <Link href="https://pywebview.flowrl.com/" target="_blank">
        Documentation
      </Link>
    </Flex>
  );
}
