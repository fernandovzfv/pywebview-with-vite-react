import Header from "./components/Header"
import { Flex } from '@radix-ui/themes'
import Tracker from "./components/Tracker"

function App() {

  return (
    <Flex direction="column" gap="4">
      <Header />
      <Tracker />
    </Flex>
  )
}

export default App
