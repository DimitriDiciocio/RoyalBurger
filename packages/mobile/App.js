import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import ContainerBurger from "./components/ContainerBurger";

export default function App() {
  return (
    <View style={styles.container}>
        <View style={[styles.flex_row, styles.gap_sm]}>
            <ContainerBurger/>
            <ContainerBurger/>
            <ContainerBurger/>
        </View>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F6F6F6',
    alignItems: 'center',
    justifyContent: 'center',
  },
  flex_row: {
      flexDirection: 'row',
  },
  gap_sm: {
      gap: 10,
  },
});
